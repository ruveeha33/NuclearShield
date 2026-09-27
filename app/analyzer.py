from __future__ import annotations

import csv
import hashlib
import io
import json
import math
import statistics
from dataclasses import asdict, dataclass
from typing import Any

from sklearn.ensemble import IsolationForest

ALLOWED_TYPES = {"network", "integrity", "access", "material", "radiation", "change"}
MAX_BYTES, MAX_RECORDS = 10_000_000, 50_000
ML_MIN_ROWS = 20
ML_FIELDS = ("value", "orig_bytes", "resp_bytes", "duration")


@dataclass(frozen=True)
class Finding:
    event_id: str
    score: int
    severity: str
    confidence: int
    engine: str
    reasons: list[str]
    contributors: list[str]
    related_events: list[str]
    requires_human_authorization: bool = True


def _pick(row: dict[str, Any], *names: str, default: Any = "") -> Any:
    lookup = {str(k).strip().lower().replace(" ", "_"): v for k, v in row.items()}
    return next((lookup[n] for n in names if n in lookup and lookup[n] not in (None, "")), default)


def _infer_type(row: dict[str, Any]) -> str:
    explicit = str(_pick(row, "event_type", "type", "category")).lower().strip()
    if explicit in ALLOWED_TYPES:
        return explicit
    haystack = " ".join(str(v).lower() for v in row.values()) + " " + " ".join(row).lower()
    terms = {
        "integrity": ("hash", "firmware", "logic", "checksum", "integrity"),
        "access": ("badge", "login", "access", "door", "identity"),
        "material": ("inventory", "material", "mca", "mass", "quantity"),
        "radiation": ("radiation", "portal", "dose", "count_rate"),
        "change": ("change", "release", "commit", "approval", "configuration"),
        "network": ("src_ip", "dst_ip", "zeek", "suricata", "network", "port", "protocol"),
    }
    return next(
        (kind for kind, words in terms.items() if any(word in haystack for word in words)),
        "network",
    )


def _truth(value: Any, default: bool = True) -> bool:
    if value in (None, ""):
        return default
    return str(value).strip().lower() in {"true", "1", "yes", "approved", "valid", "ok", "match"}


def _number(value: Any) -> float | None:
    try:
        result = float(str(value).replace(",", "").strip())
        return result if math.isfinite(result) else None
    except (TypeError, ValueError):
        return None


def parse_evidence(filename: str, raw: bytes) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    if len(raw) > MAX_BYTES:
        raise ValueError("Evidence file exceeds the 10 MB demonstration limit")
    text = raw.decode("utf-8-sig")
    lower = filename.lower()
    if lower.endswith(".json"):
        try:
            value = json.loads(text)
            records = value if isinstance(value, list) else value.get("events", value.get("records", [value] if isinstance(value, dict) else []))
        except json.JSONDecodeError:
            # Suricata EVE exports are commonly newline-delimited JSON.
            records = [json.loads(line) for line in text.splitlines() if line.strip()]
    elif lower.endswith((".jsonl", ".ndjson")):
        records = [json.loads(line) for line in text.splitlines() if line.strip()]
    elif lower.endswith(".csv"):
        records = list(csv.DictReader(io.StringIO(text)))
    elif lower.endswith(".log"):
        # Zeek ASCII logs: consume #fields and tab-separated records while ignoring metadata lines.
        lines = [line for line in text.splitlines() if line.strip()]
        field_line = next((line for line in lines if line.startswith("#fields")), None)
        if not field_line:
            raise ValueError(".log evidence requires a Zeek #fields header")
        fields = field_line.split("\t")[1:] if "\t" in field_line else field_line.split()[1:]
        records = []
        for line in lines:
            if line.startswith("#"):
                continue
            values = line.split("\t")
            records.append(dict(zip(fields, values)))
    else:
        raise ValueError("Accepted evidence formats: CSV, JSON, JSONL/NDJSON and Zeek .log")
    if not isinstance(records, list) or not records:
        raise ValueError("Evidence must contain at least one record")
    if len(records) > MAX_RECORDS:
        raise ValueError(f"Evidence contains more than {MAX_RECORDS:,} records")
    clean, rejected = [], []
    for index, raw_row in enumerate(records, 1):
        if not isinstance(raw_row, dict):
            rejected.append({"row": index, "reason": "record is not an object"})
            continue
        row = {str(k)[:80]: str(v)[:2000] for k, v in raw_row.items() if k is not None}
        if not any(str(v).strip() for v in row.values()):
            rejected.append({"row": index, "reason": "empty record"})
            continue
        event_id = str(_pick(row, "event_id", "id", "uid", "flow_id", default=f"ROW-{index:05d}"))
        source = str(
            _pick(row, "source", "sensor", "device", "host", "system", "event_type", "_path", default="uploaded-evidence")
        )
        clean.append(
            {
                **row,
                "event_id": event_id,
                "timestamp": str(
                    _pick(row, "timestamp", "time", "datetime", "date", "ts", default="unknown")
                ),
                "event_type": _infer_type(row),
                "source": source,
                "value": str(
                    _pick(
                        row,
                        "value",
                        "observed",
                        "orig_bytes",
                        "bytes_toserver",
                        "reading",
                        "count",
                        "quantity",
                        "status",
                        default="n/a",
                    )
                ),
                "baseline": str(
                    _pick(row, "baseline", "expected", "approved_value", "reference", default="n/a")
                ),
                "authorized": _truth(
                    _pick(row, "authorized", "approved", "permitted", default="true")
                ),
                "integrity": str(
                    _pick(row, "integrity", "signature_status", "hash_status", default="valid")
                ).lower(),
                "actor": str(
                    _pick(row, "actor", "user", "badge_id", "identity", default="unknown")
                ),
                "asset": str(_pick(row, "asset", "host", "device", "system", "dest_ip", "id.resp_h", default=source)),
                "raw_row": index,
            }
        )
    if not clean:
        raise ValueError("No usable evidence records were found")
    return clean, rejected


def _profiles(events: list[dict[str, Any]]) -> dict[str, tuple[float, float]]:
    groups: dict[str, list[float]] = {}
    for event in events:
        value = _number(event.get("value"))
        if value is not None:
            groups.setdefault(event["event_type"], []).append(value)
    profiles = {}
    for kind, values in groups.items():
        if len(values) >= 5:
            median = statistics.median(values)
            mad = statistics.median(abs(value - median) for value in values) or max(
                abs(median) * 0.01, 0.001
            )
            profiles[kind] = (median, mad)
    return profiles


def network_model(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Exploratory, per-upload network outlier screening; no plant-trained model."""
    network = [(index, event) for index, event in enumerate(events) if event["event_type"] == "network"]
    result: dict[str, Any] = {
        "status": "insufficient_data", "method": "scikit-learn IsolationForest",
        "minimum_rows": ML_MIN_ROWS, "network_rows": len(network), "eligible_rows": 0,
        "features": [], "outliers": [], "scores": [],
        "use_case": "Prioritize unusual numeric network evidence for human review; outliers are not confirmed attacks.",
        "training_scope": "Fits and scores only the current uploaded network evidence, with no external plant data.",
    }
    if len(network) < ML_MIN_ROWS:
        return result
    # Use real supplied numeric fields only; never invent telemetry or fill missing values.
    fields = [field for field in ML_FIELDS if sum(_number(event.get(field)) is not None for _, event in network) >= max(ML_MIN_ROWS, math.ceil(len(network) * 0.8))]
    if not fields:
        return result
    for field in fields[:]:
        values = [_number(event.get(field)) for _, event in network]
        if len({v for v in values if v is not None}) < 5:
            fields.remove(field)
    if not fields:
        return result
    eligible = [(index, event) for index, event in network if all(_number(event.get(field)) is not None for field in fields)]
    result["eligible_rows"] = len(eligible)
    result["features"] = fields
    if len(eligible) < ML_MIN_ROWS:
        return result
    matrix = [[_number(event[field]) for field in fields] for _, event in eligible]
    model = IsolationForest(n_estimators=100, contamination=0.05, random_state=42, n_jobs=1)
    model.fit(matrix)
    scores = model.decision_function(matrix)
    result["status"] = "completed"
    result["scores"] = [
        {"row_index": index, "event_id": event["event_id"], "decision_score": round(float(score), 5),
         "outlier": bool(score < 0), "values": {field: _number(event[field]) for field in fields}}
        for (index, event), score in zip(eligible, scores)
    ]
    result["outliers"] = [row for row in result["scores"] if row["outlier"]]
    return result


def analyze(events: list[dict[str, Any]], model_result: dict[str, Any] | None = None) -> list[Finding]:
    profiles, findings = _profiles(events), []
    model_result = model_result if model_result is not None else network_model(events)
    model_flags = {row["row_index"]: row for row in model_result["outliers"]}
    suspicious_access = [e for e in events if e["event_type"] == "access" and not e["authorized"]]
    for index, event in enumerate(events):
        score, reasons, contributors, engines = 0, [], [], []
        value, baseline = _number(event.get("value")), _number(event.get("baseline"))
        if value is not None and baseline is not None:
            deviation = abs(value - baseline) / max(abs(baseline), 1.0)
            if deviation >= 0.5:
                score += 50
                reasons.append("observed value differs from its declared baseline by at least 50%")
                contributors.append(f"baseline deviation {deviation:.1%}")
                engines.append("baseline-rule")
            elif deviation >= 0.2:
                score += 28
                reasons.append("observed value differs from its declared baseline by at least 20%")
                contributors.append(f"baseline deviation {deviation:.1%}")
                engines.append("baseline-rule")
        elif (
            event.get("baseline") not in ("", "n/a")
            and str(event.get("value")).lower() != str(event.get("baseline")).lower()
        ):
            score += 42
            reasons.append("observed state differs from its declared approved state")
            contributors.append("categorical state mismatch")
            engines.append("integrity-rule")
        if not event["authorized"]:
            score += 35
            reasons.append("record has no declared authorization")
            contributors.append("authorization=false")
            engines.append("authorization-rule")
        if event["integrity"] not in {"valid", "ok", "match", "true"}:
            score += 45
            reasons.append("integrity or signature evidence does not match the approved baseline")
            contributors.append(f"integrity={event['integrity']}")
            engines.append("integrity-rule")
        if value is not None and event["event_type"] in profiles:
            median, mad = profiles[event["event_type"]]
            robust_z = 0.6745 * abs(value - median) / mad
            if robust_z >= 3.5:
                score += min(35, round(robust_z * 4))
                reasons.append(
                    "median/MAD statistical check identified unusual peer-group behavior"
                )
                contributors.append(f"robust z-score {robust_z:.2f}")
                engines.append("robust-anomaly-model")
        if index in model_flags:
            flag = model_flags[index]
            score += 25
            reasons.append("Isolation Forest flagged this uploaded network observation as an outlier for human review")
            contributors.append(f"Isolation Forest decision score {flag['decision_score']:.5f} (negative means outlier)")
            engines.append("isolation-forest")
        related = []
        if event["event_type"] in {"network", "material", "radiation", "change"}:
            related = [
                a["event_id"]
                for a in suspicious_access
                if (event["actor"] != "unknown" and event["actor"] == a["actor"])
                or event["asset"] == a["asset"]
            ]
            if related:
                score += 20
                reasons.append(
                    "physical-cyber correlation links this record to unauthorized access evidence"
                )
                contributors.append(f"{len(related)} correlated access record(s)")
                engines.append("correlation-engine")
        score = min(100, score)
        if score:
            severity = (
                "critical"
                if score >= 80
                else "high"
                if score >= 55
                else "medium"
                if score >= 30
                else "low"
            )
            confidence = min(99, 55 + 9 * len(set(engines)) + min(18, len(contributors) * 4))
            findings.append(
                Finding(
                    event["event_id"],
                    score,
                    severity,
                    confidence,
                    "+".join(dict.fromkeys(engines)),
                    reasons,
                    contributors,
                    related,
                )
            )
    return sorted(findings, key=lambda item: (item.score, item.confidence), reverse=True)


def build_summary(
    events: list[dict[str, Any]], findings: list[Finding], rejected: list[dict[str, Any]],
    model_result: dict[str, Any] | None = None,
) -> dict[str, Any]:
    total = len(events) + len(rejected)
    return {
        "accepted_records": len(events),
        "rejected_records": len(rejected),
        "records_seen": total,
        "processing_coverage": round(len(events) / total * 100, 1) if total else 0,
        "finding_rate": round(len(findings) / len(events) * 100, 1) if events else 0,
        "severities": {
            level: sum(f.severity == level for f in findings)
            for level in ("critical", "high", "medium", "low")
        },
        "evidence_types": {
            kind: sum(e["event_type"] == kind for e in events) for kind in sorted(ALLOWED_TYPES)
        },
        "engines": {
            name: sum(name in f.engine.split("+") for f in findings)
            for name in (
                "baseline-rule",
                "integrity-rule",
                "authorization-rule",
                "robust-anomaly-model",
                "isolation-forest",
                "correlation-engine",
            )
        },
        "network_ml": model_result if model_result is not None else network_model(events),
        "ai_statement": "Current-file Isolation Forest screening plus explainable rules and median/MAD; no autonomous action or reactor-trained model.",
    }


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def finding_dicts(findings: list[Finding]) -> list[dict[str, Any]]:
    return [asdict(finding) for finding in findings]
