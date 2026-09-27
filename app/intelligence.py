"""Offline, exact-match indicator review for synthetic network evidence.

No external feed is fetched; supplied catalog claims are never authenticated.
"""

from __future__ import annotations

import ipaddress
import json
from typing import Any


MAX_CATALOG_BYTES = 128_000
MAX_INDICATORS = 100
FIELDS = {"source_ip": ("src_ip", "id.orig_h"),
          "destination_ip": ("dest_ip", "dst_ip", "id.resp_h"),
          "signature": ("alert.signature", "signature")}


def read_catalog(raw: bytes) -> list[dict[str, str]]:
    if len(raw) > MAX_CATALOG_BYTES:
        raise ValueError("Offline indicator file exceeds 128 KB")
    try:
        parsed = json.loads(raw.decode("utf-8-sig"))
    except (UnicodeError, json.JSONDecodeError) as exc:
        raise ValueError("Offline indicators must be valid UTF-8 JSON") from exc
    if not isinstance(parsed, dict) or not isinstance(parsed.get("indicators"), list):
        raise ValueError("Expected an object with an indicators list")
    values = parsed["indicators"]
    if not 1 <= len(values) <= MAX_INDICATORS:
        raise ValueError("Provide 1 to 100 offline indicators")
    result = []
    for index, entry in enumerate(values, 1):
        if not isinstance(entry, dict):
            raise ValueError(f"Indicator {index} is not an object")
        kind, value = entry.get("kind"), entry.get("value")
        if kind not in FIELDS or not isinstance(value, str) or not 1 <= len(value) <= 160:
            raise ValueError(f"Indicator {index} needs a supported kind and short exact value")
        if kind.endswith("_ip"):
            try:
                ipaddress.ip_address(value)
            except ValueError as exc:
                raise ValueError(f"Indicator {index} has an invalid IP address") from exc
        result.append({"id": str(entry.get("id", f"IND-{index}"))[:64],
                       "kind": kind, "value": value, "description": str(entry.get("description", ""))[:160]})
    return result


def review_indicators(events: list[dict[str, Any]], indicators: list[dict[str, str]]) -> dict[str, Any]:
    matches = []
    network = [event for event in events if event.get("event_type") == "network"]
    for event in network:
        for entry in indicators:
            if any(str(event.get(field, "")).strip() == entry["value"] for field in FIELDS[entry["kind"]]):
                matches.append({"event_id": event["event_id"], "indicator_id": entry["id"],
                                "kind": entry["kind"], "value": entry["value"],
                                "description": entry["description"]})
                if len(matches) >= 100:
                    break
        if len(matches) >= 100:
            break
    return {"network_rows": len(network), "indicators_checked": len(indicators),
            "matches": matches, "truncated": len(matches) >= 100,
            "scope": "Exact comparison with a user-supplied offline catalog. Its provenance and "
                     "accuracy are unverified; a match is not evidence of compromise."}


REVIEW_STEPS = [
    "Preserve the uploaded evidence and verify its source, timestamp and declared context.",
    "Confirm the indicator against an approved intelligence source and authorized work records.",
    "Ask qualified cyber, operations and safety personnel to assess potential consequences.",
    "If escalation is warranted, use the facility-approved response procedure outside NuclearShield.",
    "Document the authorized decision and retain supporting evidence; no automated containment occurs.",
]
