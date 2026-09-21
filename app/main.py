from __future__ import annotations

import html
import json
import os
import time
from pathlib import Path
from urllib.error import URLError
from urllib.request import urlopen

from fastapi import FastAPI, File, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

from .analyzer import analyze, build_summary, digest, finding_dicts, parse_evidence
from .store import append_audit, delete_analysis, get_analysis, list_analyses, recent_audit, save_analysis

ROOT = Path(__file__).resolve().parent
app = FastAPI(title="NuclearShield", version="1.0.8")
ingestions = Counter("nuclearshield_ingestions_total", "Evidence files processed", ["result"])
finding_count = Gauge("nuclearshield_findings", "Findings in the latest analysis", ["severity"])
engine_count = Gauge(
    "nuclearshield_findings_by_engine",
    "Findings in the latest analysis by detection engine",
    ["engine"],
)
events_processed = Counter(
    "nuclearshield_events_processed_total", "Evidence records processed", ["event_type"]
)
rows_rejected = Counter("nuclearshield_rows_rejected_total", "Evidence rows rejected")
upload_bytes = Histogram(
    "nuclearshield_upload_bytes",
    "Uploaded evidence size in bytes",
    buckets=(1_000, 10_000, 100_000, 1_000_000, 10_000_000),
)
analysis_seconds = Histogram(
    "nuclearshield_analysis_duration_seconds", "Evidence analysis duration"
)
http_requests = Counter(
    "nuclearshield_http_requests_total", "HTTP requests", ["method", "path", "status"]
)
http_seconds = Histogram(
    "nuclearshield_http_request_duration_seconds", "HTTP request duration", ["path"]
)
latest: dict = {"id": None, "filename": None, "digest": None, "events": [], "findings": []}

CONTROLS = [
    {
        "domain": "Defense in depth",
        "iec": "IEC 62645 programme and graded approach",
        "nrc": "RG 5.71 defensive architecture",
        "iaea": "NSS computer security levels and zones",
        "evidence": "zone/conduit design, passive sensor records",
    },
    {
        "domain": "Safety integrity",
        "iec": "I&C lifecycle and independence",
        "nrc": "critical digital asset controls",
        "iaea": "safety and security interface",
        "evidence": "signed baselines, one-way integrity records",
    },
    {
        "domain": "Access and safeguards",
        "iec": "access control and accountability",
        "nrc": "personnel and physical protection interfaces",
        "iaea": "nuclear material and insider controls",
        "evidence": "PACS/IAM, MC&A, radiation and cyber correlation",
    },
    {
        "domain": "Change assurance",
        "iec": "configuration management",
        "nrc": "secure lifecycle and effectiveness evaluation",
        "iaea": "sustaining a computer security programme",
        "evidence": "review, static analysis, approval and rollback records",
    },
]

DETECTION_CATALOG = {
    "network": {
        "detected": "Network activity outside the declared passive-traffic baseline",
        "sensor": "Zeek/Suricata-style passive network evidence",
        "method": "Numeric baseline-deviation rule over mirrored metadata; no packet injection",
        "measures": "Validate the mirror source and plant state, preserve the evidence, review the approved communication baseline, and escalate through the OT incident procedure if confirmed.",
    },
    "integrity": {
        "detected": "Safety software, firmware or configuration integrity mismatch",
        "sensor": "Independent safety-integrity validator through one-way evidence transfer",
        "method": "Observed state or digest compared with the declared approved baseline",
        "measures": "Do not alter the safety system from this platform. Preserve the digest, verify the approved golden baseline, invoke two-person engineering review, and recover only through the validated safety procedure.",
    },
    "access": {
        "detected": "Physical access without matching declared authorization",
        "sensor": "Synthetic PACS/IAM and work-authorization evidence",
        "method": "Authorization-state check correlated with the access event",
        "measures": "Confirm identity and work order with security operations, preserve badge and device evidence, review segregation of duties, and escalate potential insider risk through the approved safeguards process.",
    },
    "material": {
        "detected": "Nuclear material accounting value outside its declared baseline",
        "sensor": "Synthetic MC&A ledger evidence",
        "method": "Quantitative inventory-deviation rule with attributable event identity",
        "measures": "Freeze reporting changes, reconcile the source records under safeguards supervision, preserve chain of custody, and follow regulator-approved discrepancy reporting thresholds.",
    },
    "radiation": {
        "detected": "Radiation portal evidence outside its declared baseline",
        "sensor": "Synthetic radiation portal monitor evidence",
        "method": "Numeric deviation rule correlated with timestamp and source identity",
        "measures": "Verify sensor health and authorized movement context, correlate PACS and MC&A evidence, preserve the record, and let qualified radiation-protection and safeguards personnel decide the response.",
    },
    "change": {
        "detected": "Change-control state outside the declared approved baseline",
        "sensor": "Synthetic signed release and configuration-control evidence",
        "method": "Approval and integrity-state comparison against the release baseline",
        "measures": "Block promotion outside this demonstrator, verify signatures and approvals, review static-analysis evidence, and use the tested rollback plan under two-person control.",
    },
}

REPORT_FIX_CSS = (ROOT / "static" / "report.css").read_text(encoding="utf-8")


@app.middleware("http")
async def instrument(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    path = request.url.path if request.url.path.startswith("/api/") else "other"
    http_requests.labels(request.method, path, str(response.status_code)).inc()
    http_seconds.labels(path).observe(time.perf_counter() - started)
    return response


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "mode": "synthetic-demo", "control_capability": "none"}


@app.get("/api/overview")
def overview() -> dict:
    analysis = get_analysis() or latest
    findings = analysis.get("findings", [])
    return {
        "synthetic": True,
        "analysis_id": analysis.get("id"),
        "events": len(analysis.get("events", [])),
        "findings": findings,
        "severity": {
            level: sum(f["severity"] == level for f in findings)
            for level in ("critical", "high", "medium", "low")
        },
        "zones": 5,
        "diode": "evidence-only",
        "last_file": analysis.get("filename"),
        "summary": analysis.get("summary", {}),
    }


@app.get("/api/analyses")
def analyses() -> list[dict]:
    return list_analyses()


@app.get("/api/analyses/{analysis_id}")
def analysis_detail(analysis_id: str) -> dict:
    analysis = get_analysis(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@app.delete("/api/analyses/{analysis_id}")
def remove_analysis(analysis_id: str) -> dict:
    deleted = delete_analysis(analysis_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return deleted


@app.get("/api/detections")
def detections(
    analysis_id: str | None = None, event_type: str | None = None, severity: str | None = None
) -> dict:
    analysis = get_analysis(analysis_id)
    if not analysis:
        return {"analysis_id": None, "findings": []}
    events_by_id = {event["event_id"]: event for event in analysis["events"]}
    enriched = []
    for index, finding in enumerate(analysis["findings"], start=1):
        event_id = str(finding.get("event_id") or f"unknown-{index}")
        event = events_by_id.get(event_id, {})
        catalog = DETECTION_CATALOG.get(
            event.get("event_type", "network"), DETECTION_CATALOG["network"]
        )
        item = {**finding, "event": event, **catalog}
        if event_type and event.get("event_type") != event_type:
            continue
        if severity and finding.get("severity", "low") != severity:
            continue
        enriched.append(item)
    return {"analysis_id": analysis["id"], "filename": analysis["filename"], "findings": enriched}


@app.get("/api/events")
def events(
    analysis_id: str | None = None,
    event_type: str | None = None,
    search: str | None = None,
    offset: int = 0,
    limit: int = 100,
) -> dict:
    analysis = get_analysis(analysis_id)
    if not analysis:
        return {"analysis_id": None, "total": 0, "events": []}
    rows = analysis["events"]
    if event_type:
        rows = [row for row in rows if row["event_type"] == event_type]
    if search:
        needle = search.lower()
        rows = [row for row in rows if needle in json.dumps(row).lower()]
    return {
        "analysis_id": analysis["id"],
        "total": len(rows),
        "offset": offset,
        "limit": min(limit, 500),
        "events": rows[offset : offset + min(limit, 500)],
    }


@app.get("/api/ai-insights")
def ai_insights(analysis_id: str | None = None) -> dict:
    analysis = get_analysis(analysis_id)
    if not analysis:
        return {"analysis_id": None, "summary": {}, "insights": []}
    findings = analysis["findings"]
    return {
        "analysis_id": analysis["id"],
        "summary": analysis.get("summary", {}),
        "insights": [
            {
                "event_id": f["event_id"],
                "confidence": f.get("confidence", 0),
                "engine": f.get("engine", "rule"),
                "contributors": f.get("contributors", []),
                "related_events": f.get("related_events", []),
            }
            for f in findings
        ],
        "governance": {
            "autonomous_action": False,
            "human_authorization": True,
            "model_claim": "Hybrid explainable statistical inference over uploaded synthetic evidence",
        },
    }


@app.get("/api/platform-status")
def platform_status() -> dict:
    def service_status(url: str) -> str:
        try:
            with urlopen(url, timeout=0.6) as response:  # nosec B310
                return "healthy" if response.status == 200 else "unavailable"
        except (URLError, TimeoutError, OSError):
            return "unavailable"

    app_port = os.getenv("PUBLIC_APP_PORT", "8000")
    prometheus_port = os.getenv("PUBLIC_PROMETHEUS_PORT", "9090")
    grafana_port = os.getenv("PUBLIC_GRAFANA_PORT", "3000")
    return {
        "api": "healthy",
        "database": "healthy",
        "evidence_pipeline": "ready",
        "prometheus": service_status(
            os.getenv("PROMETHEUS_URL", "http://127.0.0.1:9090").rstrip("/") + "/-/ready"
        ),
        "grafana": service_status(
            os.getenv("GRAFANA_URL", "http://127.0.0.1:3000").rstrip("/") + "/api/health"
        ),
        "control_capability": "none",
        "synthetic_mode": True,
        "public_urls": {
            "application": f"http://localhost:{app_port}",
            "prometheus": f"http://localhost:{prometheus_port}",
            "grafana": f"http://localhost:{grafana_port}",
        },
    }


@app.get("/api/monitoring-summary")
def monitoring_summary() -> dict:
    history = list_analyses(100)
    selected = get_analysis()
    audit_rows = recent_audit(500)
    findings = selected.get("findings", []) if selected else []
    events = selected.get("events", []) if selected else []
    return {
        "totals": {
            "analyses": len(history),
            "records": sum(row["event_count"] for row in history),
            "findings": sum(row["finding_count"] for row in history),
            "audit_entries": len(audit_rows),
        },
        "latest": {
            "filename": selected.get("filename") if selected else None,
            "records": len(events),
            "findings": len(findings),
            "coverage": selected.get("summary", {}).get("processing_coverage", 0)
            if selected
            else 0,
            "severity": {
                level: sum(item["severity"] == level for item in findings)
                for level in ("critical", "high", "medium", "low")
            },
            "domains": {
                kind: sum(event["event_type"] == kind for event in events)
                for kind in sorted({event["event_type"] for event in events})
            },
            "engines": selected.get("summary", {}).get("engines", {}) if selected else {},
        },
        "history": history[:10],
        "prometheus_endpoint": "/metrics",
    }


@app.get("/api/network-monitoring")
def network_monitoring() -> dict:
    analysis = get_analysis()
    if not analysis:
        return {"analysis_id": None, "zeek": {"records": [], "findings": [], "protocols": {}, "conversations": {}}, "suricata": {"records": [], "findings": [], "signatures": {}, "categories": {}}, "other": [], "assets": {}, "sensor_health": {"classified": 0, "total_network": 0, "classification_percent": 0}}
    events = [e for e in analysis.get("events", []) if e.get("event_type") == "network"]
    findings = analysis.get("findings", [])
    by_id = {f.get("event_id"): f for f in findings}
    def sensor(e):
        keys = {str(k).lower() for k in e}
        source = str(e.get("source", "")).lower()
        if ({"flow_id", "app_proto", "alert", "signature", "alert.signature", "alert.category", "bytes_toserver"} & keys) or "suricata" in source or "eve" in source:
            return "suricata"
        if ({"uid", "id.orig_h", "id.resp_h", "id.orig_p", "id.resp_p", "orig_bytes", "resp_bytes", "service"} & keys) or "zeek" in source or source.endswith(".log") or source in {"conn", "dns", "notice", "http", "ssl"}:
            return "zeek"
        return "other"
    groups = {"zeek": [], "suricata": [], "other": []}
    assets, protocols, conversations, signatures, categories = {}, {}, {}, {}, {}
    for event in events:
        kind = sensor(event)
        protocol = event.get("proto") or event.get("protocol") or event.get("app_proto") or event.get("service") or "unknown"
        src_ip = event.get("src_ip") or event.get("id.orig_h") or "unknown"
        dst_ip = event.get("dest_ip") or event.get("dst_ip") or event.get("id.resp_h") or "unknown"
        signature = event.get("signature") or event.get("alert.signature") or event.get("alert") or ""
        category = event.get("alert.category") or event.get("category") or ""
        row = {
            "event_id": event.get("event_id"), "timestamp": event.get("timestamp"),
            "source": event.get("source"), "asset": event.get("asset"),
            "actor": event.get("actor"), "value": event.get("value"),
            "baseline": event.get("baseline"), "authorized": event.get("authorized"),
            "protocol": protocol, "src_ip": src_ip, "dst_ip": dst_ip,
            "src_port": event.get("src_port") or event.get("id.orig_p"),
            "dst_port": event.get("dest_port") or event.get("dst_port") or event.get("id.resp_p"),
            "signature": signature, "category": category,
            "bytes": event.get("orig_bytes") or event.get("bytes_toserver") or event.get("value"),
            "finding": by_id.get(event.get("event_id")),
        }
        groups[kind].append(row)
        asset = str(event.get("asset") or event.get("source") or "unknown")
        assets[asset] = assets.get(asset, 0) + 1
        if kind == "zeek":
            protocols[str(protocol)] = protocols.get(str(protocol), 0) + 1
            pair = f"{src_ip} → {dst_ip}"
            conversations[pair] = conversations.get(pair, 0) + 1
        if kind == "suricata":
            if signature:
                signatures[str(signature)] = signatures.get(str(signature), 0) + 1
            if category:
                categories[str(category)] = categories.get(str(category), 0) + 1
    classified = len(groups["zeek"]) + len(groups["suricata"])
    return {
        "analysis_id": analysis.get("id"), "filename": analysis.get("filename"),
        "zeek": {"records": groups["zeek"], "findings": [r for r in groups["zeek"] if r["finding"]], "protocols": protocols, "conversations": conversations},
        "suricata": {"records": groups["suricata"], "findings": [r for r in groups["suricata"] if r["finding"]], "signatures": signatures, "categories": categories},
        "other": groups["other"], "assets": assets,
        "sensor_health": {"classified": classified, "total_network": len(events), "classification_percent": round(classified / len(events) * 100) if events else 0},
    }


@app.get("/api/controls")
def controls() -> list[dict]:
    return CONTROLS


@app.get("/api/audit")
def audit(limit: int = 100, action: str | None = None, search: str | None = None) -> list[dict]:
    rows = recent_audit(min(max(limit, 1), 500))
    if action:
        rows = [row for row in rows if row["action"] == action]
    if search:
        needle = search.lower()
        rows = [row for row in rows if needle in json.dumps(row).lower()]
    return rows


@app.get("/api/audit-summary")
def audit_summary() -> dict:
    rows = recent_audit(500)
    return {
        "entries": len(rows),
        "actions": {
            name: sum(row["action"] == name for row in rows)
            for name in sorted({row["action"] for row in rows})
        },
        "actors": len({row["actor"] for row in rows}),
        "latest_timestamp": rows[0]["timestamp"] if rows else None,
        "chain_note": "Append-only demonstration log with SHA-256 evidence references",
    }


@app.post("/api/ingest")
async def ingest(file: UploadFile = File(...)) -> dict:
    started = time.perf_counter()
    try:
        raw = await file.read()
        events, rejected = parse_evidence(file.filename or "evidence", raw)
        analyzed = analyze(events)
        findings = finding_dicts(analyzed)
        summary = build_summary(events, analyzed, rejected)
    except (UnicodeError, ValueError, json.JSONDecodeError) as exc:
        ingestions.labels(result="rejected").inc()
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    evidence_digest = digest(raw)
    saved = save_analysis(
        file.filename or "evidence", evidence_digest, events, findings, summary, rejected
    )
    latest.update(saved)
    for severity in ("low", "medium", "high", "critical"):
        finding_count.labels(severity=severity).set(
            sum(f["severity"] == severity for f in findings)
        )
    for engine in (
        "baseline-rule",
        "integrity-rule",
        "authorization-rule",
        "robust-anomaly-model",
        "correlation-engine",
    ):
        engine_count.labels(engine=engine).set(
            sum(engine in f.get("engine", "").split("+") for f in findings)
        )
    for event in events:
        events_processed.labels(event_type=event["event_type"]).inc()
    rows_rejected.inc(len(rejected))
    upload_bytes.observe(len(raw))
    analysis_seconds.observe(time.perf_counter() - started)
    append_audit(
        "evidence_ingested",
        evidence_digest,
        {
            "analysis_id": saved["id"],
            "filename": file.filename,
            "events": len(events),
            "rejected": len(rejected),
            "findings": len(findings),
            "synthetic": True,
        },
    )
    ingestions.labels(result="accepted").inc()
    return {
        "synthetic": True,
        "read_only": True,
        "analysis_id": saved["id"],
        "digest": evidence_digest,
        "events": len(events),
        "rejected": rejected,
        "summary": summary,
        "findings": findings,
    }


@app.get("/api/report", response_class=HTMLResponse)
def report(analysis_id: str | None = None, print_view: bool = False) -> str:
    selected = get_analysis(analysis_id) or get_analysis() or latest
    if not isinstance(selected, dict):
        selected = {"id": "", "filename": "No analysis", "digest": "", "events": [], "findings": [], "summary": {}, "created_at": ""}
    selected.setdefault("events", [])
    selected.setdefault("findings", [])
    selected.setdefault("summary", {})
    events_by_id = {event.get("event_id", f"event-{i}"): event for i, event in enumerate(selected.get("events", [])) if isinstance(event, dict)}
    counts = {
        severity: sum(f["severity"] == severity for f in selected["findings"])
        for severity in ("critical", "high", "medium", "low")
    }
    risk = (
        "Critical review required"
        if counts["critical"]
        else "Elevated review required"
        if counts["high"]
        else "Routine review"
    )
    finding_rows = []
    detail_sections = []
    for index, finding in enumerate([f for f in selected.get("findings", []) if isinstance(f, dict)], 1):
        event_id = str(finding.get("event_id", f"unknown-{index}"))
        event = events_by_id.get(event_id, {})
        event_type = event.get("event_type", "network")
        catalog = DETECTION_CATALOG.get(event_type, DETECTION_CATALOG["network"])
        reasons = "; ".join(finding["reasons"])
        finding_rows.append(
            f"<tr><td>NS-{index:03}</td><td>{html.escape(event_id)}</td>"
            f"<td><span class='tag {finding.get('severity', 'low')}'>{finding.get('severity', 'low')}</span></td>"
            f"<td>{finding.get('score', 0)}/100 · {finding.get('confidence', 0)}% confidence</td><td>{html.escape(catalog['detected'])}</td>"
            f"<td>{html.escape(catalog['sensor'])}</td></tr>"
        )
        detail_sections.append(f"""
        <article class='finding-card'>
          <div class='finding-head'><div><span class='finding-id'>NS-{index:03}</span><h3>{html.escape(catalog["detected"])}</h3></div><span class='tag {finding.get("severity", "low")}'>{finding.get("severity", "low")} · {finding["score"]}</span></div>
          <dl><div><dt>Evidence event</dt><dd>{html.escape(event_id)} · {html.escape(event_type.upper())}</dd></div><div><dt>Detection engine</dt><dd>{html.escape(finding.get("engine", "rule"))} · {finding.get("confidence", 0)}% confidence</dd></div><div><dt>Detected using</dt><dd>{html.escape(catalog["sensor"])}</dd></div><div><dt>Detection method</dt><dd>{html.escape(catalog["method"])}</dd></div><div><dt>Why it triggered</dt><dd>{html.escape(reasons)}</dd></div><div><dt>Contributors</dt><dd>{html.escape("; ".join(finding.get("contributors", [])))}</dd></div><div><dt>Observed / baseline</dt><dd>{html.escape(str(event.get("value", "n/a")))} / {html.escape(str(event.get("baseline", "n/a")))}</dd></div><div><dt>Source</dt><dd>{html.escape(str(event.get("source", "n/a")))}</dd></div></dl>
          <div class='measure'><strong>Recommended defensive measures</strong><p>{html.escape(catalog["measures"])}</p></div>
          <p class='authorization'><strong>Decision gate:</strong> Human and safety authorization required. NuclearShield provides evidence and prioritization only.</p>
        </article>""")
    rows = (
        "".join(finding_rows)
        or "<tr><td colspan='6'>No findings loaded. Ingest the synthetic sample first.</td></tr>"
    )
    details = (
        "".join(detail_sections)
        or "<div class='empty'>No detailed findings are available until evidence is ingested.</div>"
    )
    audit_rows = (
        "".join(
            f"<tr><td>{html.escape(a['timestamp'])}</td><td>{html.escape(a['action'])}</td><td><code>{html.escape(a['evidence_digest'][:16])}…</code></td><td>{html.escape(a['actor'])}</td></tr>"
            for a in recent_audit(10)
        )
        or "<tr><td colspan='4'>No audit entries yet.</td></tr>"
    )
    controls = "".join(
        f"<tr><td>{html.escape(c['domain'])}</td><td>{html.escape(c['iec'])}</td><td>{html.escape(c['nrc'])}</td><td>{html.escape(c['iaea'])}</td><td>{html.escape(c['evidence'])}</td></tr>"
        for c in CONTROLS
    )
    auto_print = "<script>window.addEventListener('load',()=>window.print())</script>" if print_view else ""
    return f"""<!doctype html><html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>NuclearShield detailed assurance report</title><style>{REPORT_FIX_CSS}
    :root{{--deep:#0d2824;--teal:#39766c;--paper:#f3f6f4;--line:#ccd8d4;--amber:#d69b32;--red:#9d3030}}*{{box-sizing:border-box}}body{{margin:0;font:15px/1.55 Inter,Segoe UI,system-ui;color:#14231f;background:var(--paper)}}header{{background:var(--deep);color:white;padding:46px max(5vw,28px)}}header .top{{display:flex;justify-content:space-between;gap:24px;align-items:start;max-width:1250px;margin:auto}}.brand{{display:flex;align-items:center;gap:12px;letter-spacing:.14em;font-weight:800;color:#a8d4cb}}.brand img{{width:54px;height:54px;background:#eef7f4;border-radius:14px;padding:7px}}.brand-copy{{display:grid;gap:2px}}.brand-copy strong{{font-size:1.15rem;color:#fff;letter-spacing:.02em}}.brand-copy span{{font-size:.68rem;letter-spacing:.14em;color:#a8d4cb}}.cap-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}.cap-grid article{{background:#fff;border:1px solid var(--line);border-radius:12px;padding:18px;border-top:3px solid var(--teal)}}.cap-grid article:nth-child(2){{border-top-color:#2878b8}}.cap-grid article:nth-child(3){{border-top-color:#d69b32}}.cap-grid article:nth-child(4){{border-top-color:#7167c7}}.cap-grid article:nth-child(5){{border-top-color:#20a6b5}}.cap-grid article:nth-child(6){{border-top-color:#4c9b70}}.cap-grid b{{display:block;margin-bottom:7px}}.cap-grid p{{margin:0;color:#526660;font-size:.86rem}}h1{{font-size:clamp(2.4rem,5vw,4.8rem);line-height:1;margin:38px 0 16px;letter-spacing:-.05em}}header p{{color:#c2d4d0;max-width:700px}}.classification{{border:1px solid #41655f;border-radius:999px;padding:8px 14px;font-size:.72rem;letter-spacing:.1em}}main{{max-width:1250px;margin:auto;padding:38px max(5vw,28px) 80px}}.notice{{padding:18px 20px;background:#fff4d8;border-left:5px solid var(--amber);margin-bottom:28px}}.cards{{display:grid;grid-template-columns:2fr repeat(4,1fr);gap:12px;margin:28px 0}}.card{{background:white;border:1px solid var(--line);border-radius:12px;padding:18px}}.card span{{display:block;color:#5d706b;font-size:.73rem;text-transform:uppercase;letter-spacing:.08em}}.card strong{{display:block;font-size:1.45rem;margin-top:10px}}h2{{font-size:1.75rem;margin:52px 0 18px;border-bottom:2px solid var(--deep);padding-bottom:10px}}h3{{margin:4px 0;font-size:1.25rem}}table{{width:100%;border-collapse:collapse;background:white;font-size:.85rem}}th,td{{padding:11px;border:1px solid var(--line);text-align:left;vertical-align:top}}th{{background:var(--deep);color:white}}.table-wrap{{overflow-x:auto}}.tag{{display:inline-block;border-radius:999px;padding:4px 8px;text-transform:uppercase;font-size:.68rem;font-weight:800;letter-spacing:.07em;background:#e4ece9}}.tag.critical{{background:#f4dada;color:#842222}}.tag.high{{background:#f8e6c5;color:#825410}}.tag.medium{{background:#dcedea;color:#285e55}}.finding-card{{background:white;border:1px solid var(--line);border-radius:15px;padding:24px;margin:16px 0;break-inside:avoid}}.finding-head{{display:flex;justify-content:space-between;gap:20px}}.finding-id{{color:var(--teal);font-size:.72rem;font-weight:800;letter-spacing:.1em}}dl{{display:grid;grid-template-columns:1fr 1fr;gap:0;margin:22px 0}}dl div{{border-top:1px solid var(--line);padding:12px 8px}}dt{{font-size:.72rem;text-transform:uppercase;letter-spacing:.07em;color:#61746f}}dd{{margin:5px 0 0}}.measure{{background:#e7f0ed;padding:16px;border-left:4px solid var(--teal)}}.measure p{{margin:5px 0}}.authorization{{color:#6c541d;background:#fff7e6;padding:12px}}.method-grid{{display:grid;grid-template-columns:repeat(2,1fr);gap:14px}}.method-grid article{{background:white;border-top:3px solid var(--teal);padding:20px}}.method-grid h3{{font-size:1rem}}.method-grid p{{color:#526660}}.limitations{{border:1px solid var(--line);padding:20px;background:white}}footer{{background:#0a1c19;color:#a9c3bd;padding:24px max(5vw,28px)}}code{{word-break:break-all}}@media(max-width:850px){{.cap-grid{{grid-template-columns:1fr}}.cards{{grid-template-columns:1fr 1fr}}.cards .card:first-child{{grid-column:1/-1}}dl,.method-grid{{grid-template-columns:1fr}}.finding-head,.top{{flex-direction:column}}}}@media print{{body{{background:white}}header{{padding:28px}}main{{padding:20px}}.finding-card{{break-inside:avoid}}}}
    .report-tools{{position:relative;z-index:1;display:flex;justify-content:flex-end;gap:8px;padding:10px max(5vw,28px);background:#e5ece9;border-bottom:1px solid var(--line)}}.report-tools button,.report-tools a{{border:0;border-radius:999px;padding:9px 14px;background:var(--deep);color:white;font:600 13px Inter,Segoe UI,sans-serif;text-decoration:none;cursor:pointer}}@media print{{.report-tools{{display:none}}}}
    
    /* Preserve report visual identity in browser/PDF printing. */
    *{{-webkit-print-color-adjust:exact!important;print-color-adjust:exact!important}}
    @page{{margin:10mm;background:#f4f7f6}}
    @media print{{
      html,body{{background:#f4f7f6!important}}
      header{{background:#0b302a!important;color:#fff!important}}
      header h1,.brand-copy strong{{color:#fff!important}}
      header p{{color:#d8ebe6!important}}
      .classification{{color:#fff!important;border-color:#50736c!important}}
      .notice{{background:#fff3d6!important;border-left-color:#d79a25!important}}
      .card,.finding-card,.method-grid article,.limitations{{background:#fff!important}}
      .measure{{background:#e7f0ed!important}}
      .authorization{{background:#fff7e6!important;color:#6c541d!important}}
      footer{{background:#0a1c19!important;color:#a9c3bd!important}}
    }}
</style></head><body><div class='report-tools'><button onclick='window.print()'>Print report</button><a href='/api/report/download?analysis_id={html.escape(str(selected.get("id")))}'>Download HTML</a></div><header><div class='top'><div><div class='brand'><img src='data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA0OCA0OCIgcm9sZT0iaW1nIiBhcmlhLWxhYmVsbGVkYnk9InRpdGxlIj4KICA8dGl0bGUgaWQ9InRpdGxlIj5OdWNsZWFyIHNhZmV0eSBzeW1ib2w8L3RpdGxlPgogIDxyZWN0IHg9IjMiIHk9IjMiIHdpZHRoPSI0MiIgaGVpZ2h0PSI0MiIgcng9IjkiIGZpbGw9IiMxMDJkMjgiLz4KICA8Y2lyY2xlIGN4PSIyNCIgY3k9IjI0IiByPSIxNy41IiBmaWxsPSJub25lIiBzdHJva2U9IiM2M2I3YTciIHN0cm9rZS13aWR0aD0iMiIvPgogIDxnIGZpbGw9IiM2M2I3YTciPgogICAgPHBhdGggZD0iTTIxLjIgMTguNSAxNSA4LjdBMTggMTggMCAwIDEgMzMgOC43bC02LjIgOS44YTcgNyAwIDAgMC01LjYgMFoiLz4KICAgIDxwYXRoIGQ9Ik0yMS4yIDE4LjUgMTUgOC43QTE4IDE4IDAgMCAxIDMzIDguN2wtNi4yIDkuOGE3IDcgMCAwIDAtNS42IDBaIiB0cmFuc2Zvcm09InJvdGF0ZSgxMjAgMjQgMjQpIi8+CiAgICA8cGF0aCBkPSJNMjEuMiAxOC41IDE1IDguN0ExOCAxOCAwIDAgMSAzMyA4LjdsLTYuMiA5LjhhNyA3IDAgMCAwLTUuNiAwWiIgdHJhbnNmb3JtPSJyb3RhdGUoMjQwIDI0IDI0KSIvPgogIDwvZz4KICA8Y2lyY2xlIGN4PSIyNCIgY3k9IjI0IiByPSI0LjIiIGZpbGw9IiNkN2E0NDkiLz4KPC9zdmc+Cg==' alt='NuclearShield logo'><div class='brand-copy'><strong>NuclearShield</strong><span>DETAILED ASSURANCE REPORT</span></div></div><h1>Evidence assurance & threat review</h1><p>Unified defensive analysis covering passive SCADA evidence, safety integrity, nuclear-material safeguards, explainable AI threat detection, DevSecOps assurance, compliance evidence and monitored platform health.</p></div><span class='classification'>SYNTHETIC · EDUCATIONAL · READ-ONLY</span></div></header><main>
    <p class='notice'><strong>Synthetic demonstration evidence.</strong> This report contains no real nuclear, SCADA, process, personnel or material data. NuclearShield has no control capability and does not claim regulatory certification.</p>
    <section class='cards'><div class='card'><span>Overall review status</span><strong>{risk}</strong></div><div class='card'><span>Evidence records</span><strong>{len(selected["events"])}</strong></div><div class='card'><span>Critical</span><strong>{counts["critical"]}</strong></div><div class='card'><span>High</span><strong>{counts["high"]}</strong></div><div class='card'><span>Medium</span><strong>{counts["medium"]}</strong></div></section>
    <h2>1. Executive summary</h2><p>NuclearShield validated {len(selected["events"])} synthetic evidence records and produced {len(selected["findings"])} review findings. Findings identify declared baseline, integrity or authorization deviations. Scores rank review priority; they do not diagnose a reactor condition or authorize containment.</p>
    <h2>2. Scope and evidence provenance</h2><div class='table-wrap'><table><tr><th>Analysis ID</th><td>{html.escape(str(selected.get("id")))}</td></tr><tr><th>Input file</th><td>{html.escape(str(selected["filename"]))}</td></tr><tr><th>SHA-256 evidence digest</th><td><code>{html.escape(str(selected["digest"]))}</code></td></tr><tr><th>Accepted evidence classes</th><td>Network, integrity, access, material, radiation and change-control records</td></tr><tr><th>Processing boundary</th><td>Offline CSV/JSON ingestion; no live plant connection and no command endpoint</td></tr></table></div>
    <h2>3. Platform capability coverage</h2><div class='cap-grid'><article><b>SCADA protection</b><p>Passive OT/network evidence, asset visibility, source distribution, baseline deviation and evidence-linked anomaly review.</p></article><article><b>Safety-system integrity</b><p>Approved-state, authorization and integrity evidence are evaluated without any write-back capability.</p></article><article><b>Material safeguards</b><p>PACS/IAM, MC&amp;A and radiation evidence are correlated by shared actor and asset context.</p></article><article><b>AI threat detection</b><p>Rule, robust-anomaly and correlation findings are explained with confidence, contributors, reasons and human-gated alert review.</p></article><article><b>Monitoring</b><p>Zeek-style and Suricata-style evidence feeds are combined with application metrics, Prometheus targets/queries and Grafana telemetry.</p></article><article><b>DevSecOps & governance</b><p>Change/integrity evidence, controlled delivery gates, report history, deletion controls, audit evidence and framework mappings support traceable review.</p></article></div>
    <h2>4. Detection register</h2><div class='table-wrap'><table><thead><tr><th>Finding</th><th>Event</th><th>Severity</th><th>Score</th><th>What was detected</th><th>Detected using</th></tr></thead><tbody>{rows}</tbody></table></div>
    <h2>5. Detailed findings and measures</h2>{details}
    <h2>6. Detection methodology</h2><div class='method-grid'><article><h3>Passive network evidence</h3><p>Zeek/Suricata-style records represent mirrored metadata. The platform compares declared values with baselines without injecting traffic.</p></article><article><h3>Safety integrity evidence</h3><p>Logic, firmware and configuration states compare with an approved baseline represented in the evidence file. Evidence crosses outward conceptually through a data diode.</p></article><article><h3>Physical-cyber and MC&A correlation</h3><p>Access authorization, device identity, material accounting and radiation records are correlated by shared actor or asset. The demo does not infer real material movement.</p></article><article><h3>AI-assisted anomaly analysis</h3><p>A robust median and median-absolute-deviation model identifies peer-group outliers when at least five comparable numeric records exist. Results include confidence and contributors, cannot take action, and require human and safety authorization.</p></article></div>
    <h2>7. Defense measures</h2><ol><li><strong>Preserve independence:</strong> keep monitoring outside safety functions and export safety evidence in one direction.</li><li><strong>Validate before escalation:</strong> confirm evidence quality, sensor health, plant state and authorized work context.</li><li><strong>Protect provenance:</strong> retain hashes, trusted timestamps, access records and an attributable chain of custody.</li><li><strong>Authorize narrowly:</strong> require qualified cyber, operations, safety and safeguards roles according to the event.</li><li><strong>Recover predictably:</strong> use approved procedures, signed baselines, tested rollback and post-event effectiveness review.</li></ol>
    <h2>8. Framework evidence mapping</h2><div class='table-wrap'><table><thead><tr><th>Control domain</th><th>IEC 62645 theme</th><th>NRC RG 5.71 theme</th><th>IAEA theme</th><th>Demonstration evidence</th></tr></thead><tbody>{controls}</tbody></table></div><p><small>This mapping supports learning and design discussion only. It does not establish compliance.</small></p>
    <h2>9. Audit trail</h2><div class='table-wrap'><table><thead><tr><th>Timestamp</th><th>Action</th><th>Evidence digest</th><th>Actor</th></tr></thead><tbody>{audit_rows}</tbody></table></div>
    <h2>10. Limitations and decision authority</h2><div class='limitations'><p>The dataset, identifiers and values are fictional. The rules are illustrative and not validated for nuclear operations. The platform does not inspect real packets, verify a physical data diode, control safety equipment, track real nuclear material or replace qualified authorities.</p><p><strong>Required disposition:</strong> Qualified people interpret each finding, confirm context and apply only approved safety-preserving procedures.</p></div>
    </main><footer>© 2026 NuclearShield. All rights reserved. · Detailed synthetic evidence assurance report</footer>{auto_print}</body></html>"""


@app.get("/api/report/download")
def download_report(analysis_id: str | None = None) -> Response:
    document = report(analysis_id=analysis_id)
    return Response(
        document,
        media_type="text/html",
        headers={"Content-Disposition": "attachment; filename=nuclearshield-assurance-report.html"},
    )


@app.get("/metrics")
def metrics() -> Response:
    # Restore latest-analysis gauges from persisted evidence after application restarts.
    selected = get_analysis() or {"findings": []}
    for severity in ("low", "medium", "high", "critical"):
        finding_count.labels(severity=severity).set(
            sum(f["severity"] == severity for f in selected["findings"])
        )
    for engine in (
        "baseline-rule",
        "integrity-rule",
        "authorization-rule",
        "robust-anomaly-model",
        "correlation-engine",
    ):
        engine_count.labels(engine=engine).set(
            sum(engine in f.get("engine", "").split("+") for f in selected["findings"])
        )
    for result in ("accepted", "rejected"):
        ingestions.labels(result=result)
    for domain in ("network", "integrity", "access", "material", "radiation", "change"):
        events_processed.labels(event_type=domain)
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


app.mount("/", StaticFiles(directory=ROOT / "static", html=True), name="static")
