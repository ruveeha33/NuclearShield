"""Finite, offline assurance demonstrations over uploaded synthetic evidence.

These checks cannot connect to or control an operational system. The gateway
model verifies a software policy, not the properties of a physical data diode.
"""

from __future__ import annotations

from itertools import product
from typing import Any


SOURCES = ("safety-replica", "pacs-export", "mca-export", "analytics")
DESTINATIONS = ("analytics", "safety-replica", "pacs-export", "mca-export")
KINDS = ("evidence", "command", "configuration")


def gateway_allows(source: str, destination: str, kind: str) -> bool:
    """Model outbound evidence only; there is no transport or write operation."""
    return source in SOURCES[:-1] and destination == "analytics" and kind == "evidence"


def check_gateway_policy() -> dict[str, Any]:
    cases = [
        {"source": source, "destination": destination, "kind": kind,
         "permitted": gateway_allows(source, destination, kind)}
        for source, destination, kind in product(SOURCES, DESTINATIONS, KINDS)
    ]
    violations = [case for case in cases if case["permitted"] and
                  (case["kind"] != "evidence" or case["destination"] != "analytics"
                   or case["source"] == "analytics")]
    assert len(cases) == 48
    return {"status": "pass" if not violations else "fail", "states_checked": len(cases),
            "outbound_evidence_paths": sum(case["permitted"] for case in cases),
            "inbound_or_control_allowed": bool(violations), "violations": violations,
            "scope": "Exhaustive finite check of this application's simulated gateway policy; "
                     "not a physical diode, air gap, or verification of nuclear safety code."}


def check_change_review_policy() -> dict[str, Any]:
    """Enumerate four binary review conditions for a demonstration gate."""
    cases = []
    for approved, signature_valid, independent_reviewer, safety_independent in product((False, True), repeat=4):
        review_ready = approved and signature_valid and independent_reviewer and safety_independent
        cases.append((approved, signature_valid, independent_reviewer,
                      safety_independent, review_ready))
    violations = [case for case in cases if case[4] and not all(case[:4])]
    return {"status": "pass" if not violations else "fail", "states_checked": len(cases),
            "review_ready_states": sum(case[4] for case in cases),
            "violations": violations,
            "scope": "Exhaustive bounded check of a four-condition software review gate. "
                     "No deployment or safety-system command is produced; not formal "
                     "verification of plant firmware or a licensed safety function."}


def _numeric(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def offline_safeguards(events: list[dict[str, Any]]) -> dict[str, Any]:
    """Inspect normalized offline PACS/MC&A exports without inferring intent."""
    access = [e for e in events if e.get("event_type") == "access"]
    material = [e for e in events if e.get("event_type") == "material"]
    unexplained = []
    for row in material:
        observed, baseline = _numeric(row.get("value")), _numeric(row.get("baseline"))
        if observed is not None and baseline is not None and observed != baseline:
            unexplained.append({"event_id": row["event_id"], "asset": row.get("asset"),
                                "difference": round(observed - baseline, 5)})
    links = []
    for a in access:
        for m in material:
            shared_actor = a.get("actor") not in (None, "", "unknown") and a.get("actor") == m.get("actor")
            shared_asset = a.get("asset") not in (None, "", "unknown") and a.get("asset") == m.get("asset")
            if shared_actor or shared_asset:
                links.append({"access_id": a["event_id"], "material_id": m["event_id"],
                              "basis": "actor" if shared_actor else "asset",
                              "access_authorized": a.get("authorized", True)})
    return {"access_records": len(access), "material_records": len(material),
            "inventory_differences": unexplained, "matched_records": links[:100],
            "scope": "Offline, uploaded PACS-like and MC&A-like evidence only. "
                     "Differences and joins are review prompts, not verified material movement or insider intent."}


def integrity_snapshots(analyses: list[dict[str, Any]]) -> dict[str, Any]:
    """Compare approved state and integrity across stored uploads in time order."""
    timeline: dict[str, list[dict[str, Any]]] = {}
    for analysis in sorted(analyses, key=lambda a: (a["created_at"], a["id"])):
        for event in analysis.get("events", []):
            if event.get("event_type") != "integrity":
                continue
            asset = str(event.get("asset") or "unknown")
            timeline.setdefault(asset, []).append({
                "analysis_id": analysis["id"], "file": analysis["filename"],
                "time": analysis["created_at"], "event_id": event["event_id"],
                "observed": event.get("value"), "approved": event.get("baseline"),
                "declared_integrity": event.get("integrity"),
                "deviation": (event.get("value") != event.get("baseline")
                              or event.get("integrity") not in {"valid", "ok", "match", "true"}),
            })
    changes = []
    for asset, items in timeline.items():
        for previous, current in zip(items, items[1:]):
            if previous["analysis_id"] != current["analysis_id"] and previous["observed"] != current["observed"]:
                changes.append({"asset": asset, "previous": previous, "current": current})
    return {"assets": len(timeline), "snapshots": sum(map(len, timeline.values())),
            "changed_observations": changes[:100], "timeline": timeline,
            "scope": "Checks uploaded snapshots from up to 50 recent retained analyses when a user supplies a new file; "
                     "not continuous monitoring of safety firmware or a trusted signed baseline."}
