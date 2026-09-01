import json

from nuclearshield.model import FacilityState
from nuclearshield.reporting import build_report, save_report


def test_report_contains_exam_domains():
    state = FacilityState(scenario="combined")
    report = build_report(state)
    assert report["classification"] == "EDUCATIONAL SIMULATION / SYNTHETIC DATA"
    assert "safety_assurance" in report
    assert "cyber_defense" in report
    assert "safeguards" in report
    assert "assurance" in report
    assert "No real nuclear" in report["safety_boundary"]


def test_report_exports_json_and_text(tmp_path):
    state = FacilityState(scenario="material-variance", material_accounting_ok=False, material_balance_delta=0.12)
    json_path, txt_path = save_report(state, tmp_path)
    assert json_path.exists()
    assert txt_path.exists()
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["scenario"] == "material-variance"
    assert any("MC&A" in finding for finding in payload["findings"])
