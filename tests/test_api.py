from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_states_no_control_capability():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["control_capability"] == "none"


def test_report_labels_synthetic_evidence():
    response = client.get("/api/report")
    assert response.status_code == 200
    assert "Synthetic demonstration evidence" in response.text
    assert "What was detected" in response.text
    assert "Detected using" in response.text
    assert "Detailed findings and measures" in response.text
    assert "Framework evidence mapping" in response.text
    assert "Print report" in response.text
    assert "Download HTML" in response.text


def test_report_download_is_an_html_attachment():
    response = client.get("/api/report/download")
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert "attachment;" in response.headers["content-disposition"]
    assert "nuclearshield-assurance-report.html" in response.headers["content-disposition"]


def test_upload_persists_analysis_and_populates_dynamic_views(tmp_path, monkeypatch):
    monkeypatch.setenv("NUCLEARSHIELD_DATA_DIR", str(tmp_path))
    raw = b"event_id,timestamp,event_type,source,value,baseline,authorized,integrity\nE-DYNAMIC,2026-01-01T00:00:00Z,network,passive-sensor,90,10,true,valid\n"
    response = client.post("/api/ingest", files={"file": ("evidence.csv", raw, "text/csv")})
    assert response.status_code == 200
    analysis_id = response.json()["analysis_id"]
    detail = client.get(f"/api/analyses/{analysis_id}").json()
    detections = client.get(f"/api/detections?analysis_id={analysis_id}").json()
    report = client.get(f"/api/report?analysis_id={analysis_id}")
    assert detail["event_count"] == 1
    assert detections["findings"][0]["event_id"] == "E-DYNAMIC"
    assert "Zeek/Suricata-style passive network evidence" in report.text


def test_platform_status_is_truthful():
    response = client.get("/api/platform-status")
    assert response.status_code == 200
    assert response.json()["prometheus"] in {"healthy", "unavailable"}


def test_monitoring_and_audit_pages_have_dynamic_api_data(tmp_path, monkeypatch):
    monkeypatch.setenv("NUCLEARSHIELD_DATA_DIR", str(tmp_path))
    raw = b"event_id,timestamp,event_type,source,value,baseline\nM-1,t,network,s,50,10\n"
    assert client.post("/api/ingest", files={"file": ("monitor.csv", raw)}).status_code == 200
    monitoring = client.get("/api/monitoring-summary")
    audit = client.get("/api/audit-summary")
    searched = client.get("/api/audit?search=monitor.csv")
    assert monitoring.status_code == 200
    assert monitoring.json()["totals"]["analyses"] == 1
    assert monitoring.json()["latest"]["records"] == 1
    assert audit.json()["entries"] == 1
    assert searched.json()[0]["details"]["filename"] == "monitor.csv"
