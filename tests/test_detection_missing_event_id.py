from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/main.py").read_text(encoding="utf-8")

def test_detection_fallback_event_id_has_defined_index():
    assert 'for index, finding in enumerate(analysis["findings"], start=1):' in MAIN
    assert 'finding.get("event_id") or f"unknown-{index}"' in MAIN
