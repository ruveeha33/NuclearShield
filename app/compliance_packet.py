"""Local, evidence-scoped exam packet; not an official regulatory submission."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .assurance import offline_safeguards


DOMAINS = (
    ("SCADA and I&C evidence", ("network",), "IEC 62645 / NRC RG 5.71 / IAEA guidance"),
    ("Safety integrity evidence", ("integrity",), "IEC 62645 / IAEA safety-security interface"),
    ("Material safeguards evidence", ("access", "material", "radiation"), "IAEA safeguards themes"),
    ("Controlled change evidence", ("change",), "NRC RG 5.71 / configuration management themes"),
)


def build_packet(analysis: dict[str, Any], audit: list[dict[str, Any]]) -> dict[str, Any]:
    events, findings = analysis["events"], analysis["findings"]
    counts = {kind: sum(e.get("event_type") == kind for e in events)
              for kind in ("network", "integrity", "access", "material", "radiation", "change")}
    mapping = [{"domain": name, "theme": standard,
                "evidence_records": sum(counts[kind] for kind in kinds),
                "coverage": "evidence present" if any(counts[kind] for kind in kinds) else "no evidence in upload"}
               for name, kinds, standard in DOMAINS]
    safeguards = offline_safeguards(events)
    packet = {
        "title": "NuclearShield local evidence and safeguards review packet",
        "classification": "SYNTHETIC TRAINING DATA / NOT FOR REGULATORY SUBMISSION",
        "analysis": {"id": analysis["id"], "created_at": analysis["created_at"],
                     "filename": analysis["filename"],
                     "uploaded_file_sha256_recorded_at_ingest": analysis["digest"],
                     "accepted_records": len(events), "rejected_records": len(analysis.get("rejected", []))},
        "evidence_counts": counts,
        "control_theme_mapping": mapping,
        "finding_references": [{"event_id": f["event_id"], "severity": f["severity"],
                                "engine": f["engine"], "reasons": f.get("reasons", [])}
                               for f in findings],
        "safeguards_review": {"access_records": safeguards["access_records"],
                              "material_records": safeguards["material_records"],
                              "declared_inventory_differences": safeguards["inventory_differences"],
                              "matched_evidence": safeguards["matched_records"]},
        "audit_references": [{"id": a["id"], "time": a["timestamp"], "action": a["action"],
                              "evidence_digest": a["evidence_digest"]} for a in audit],
        "limitations": [
            "Mapping represents evidence presence only; it is not IEC, NRC or IAEA compliance.",
            "Input is fictional or safely exported offline evidence, not facility telemetry.",
            "Inventory differences and access joins require qualified human verification.",
            "The original uploaded file is not retained in this packet; its recorded digest cannot be reverified here.",
            "There is no regulator submission, signed report, immutable audit store or plant-control action.",
        ],
    }
    canonical = json.dumps(packet, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    packet["packet_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    packet["hash_scope"] = "SHA-256 of this JSON object before packet_sha256 and hash_scope are added; not a signature"
    return packet
