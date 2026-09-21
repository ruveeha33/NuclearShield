from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

ROOT=Path(__file__).resolve().parents[1]
CSS=(ROOT/"app/static/styles.css").read_text(encoding="utf-8")
JS=(ROOT/"app/static/app.js").read_text(encoding="utf-8")

def test_report_and_download_do_not_crash():
    c=TestClient(app)
    assert c.get("/api/report").status_code == 200
    assert c.get("/api/report/download").status_code == 200

def test_compact_trust_architecture_replaces_old_card_block():
    assert "TRUST ARCHITECTURE" in JS
    assert "trust-path" in JS
    assert "assurance-signature" not in JS
    assert "margin-bottom:20px!important" in CSS
