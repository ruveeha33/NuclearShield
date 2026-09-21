from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CSS=(ROOT/"app/static/styles.css").read_text(encoding="utf-8")
JS=(ROOT/"app/static/app.js").read_text(encoding="utf-8")

def test_landing_has_no_large_gap_before_trust_architecture():
    assert ".landing-proof{" in CSS
    assert "margin-bottom:0!important" in CSS
    assert "padding-bottom:18px!important" in CSS
    assert "padding:18px 5vw 0" in CSS

def test_old_assurance_card_design_is_retired():
    assert ".assurance-signature{display:none!important}" in CSS
    assert "TRUST ARCHITECTURE" in JS
    assert "From evidence to a defensible human decision." in JS

def test_trust_path_is_compact_and_aligned():
    assert "min-height:104px" in CSS
    assert "grid-template-columns:1fr auto 1fr auto 1fr auto 1fr" in CSS
