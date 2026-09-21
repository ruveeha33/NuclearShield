from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "app/static/styles.css").read_text(encoding="utf-8")
JS = (ROOT / "app/static/app.js").read_text(encoding="utf-8")
MAIN = (ROOT / "app/main.py").read_text(encoding="utf-8")

def test_sensor_consoles_are_equal_fixed_height_and_scroll():
    assert ".sensor-console{" in CSS
    assert "height:390px" in CSS
    assert "overflow-y:scroll" in CSS
    assert "scrollbar-gutter:stable" in CSS

def test_landing_lifecycle_card_is_compact():
    assert "padding:30px clamp(28px,4vw,54px)" in CSS
    assert "margin:0 auto 18px" in CSS

def test_audit_can_delete_linked_analysis_without_deleting_audit_history():
    assert "Delete analyzed file" in JS
    assert 'state.analyses.find(x=>x.digest===a.evidence_digest)' in JS
    assert '"analysis_id": saved["id"]' in MAIN
