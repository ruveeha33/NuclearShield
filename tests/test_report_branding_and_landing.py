from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAIN=(ROOT/"app/main.py").read_text(encoding="utf-8")
JS=(ROOT/"app/static/app.js").read_text(encoding="utf-8")
CSS=(ROOT/"app/static/styles.css").read_text(encoding="utf-8")

def test_report_logo_is_embedded_for_offline_download():
    assert "data:image/svg+xml;base64," in MAIN

def test_print_preserves_report_colors():
    assert "-webkit-print-color-adjust:exact!important" in MAIN
    assert "print-color-adjust:exact!important" in MAIN

def test_landing_safety_authority_is_prominent_and_closes_with_boundary():
    assert "font-size:clamp(1.3rem,2.1vw,2rem)" in CSS
    assert "TRUST ARCHITECTURE" in JS
    assert "From evidence to a defensible human decision." in JS
    assert "READ ONLY BOUNDARY" in JS
