from fastapi.testclient import TestClient
from app.main import app


def test_latest_metrics_restore_from_database(tmp_path, monkeypatch):
    monkeypatch.setenv("NUCLEARSHIELD_DATA_DIR", str(tmp_path))
    from app.store import save_analysis

    save_analysis(
        "restored.csv",
        "demo-digest",
        [],
        [{"event_id": "R1", "severity": "critical", "engine": "integrity-rule"}],
    )
    response = TestClient(app).get("/metrics")
    assert response.status_code == 200
    assert 'nuclearshield_findings{severity="critical"} 1.0' in response.text
    assert 'nuclearshield_findings_by_engine{engine="integrity-rule"} 1.0' in response.text
    assert 'nuclearshield_ingestions_total{result="rejected"}' in response.text


def test_service_health_uses_configured_hosts(monkeypatch):
    from app import main

    urls = []

    class Healthy:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

    def probe(url, timeout):
        urls.append(url)
        return Healthy()

    monkeypatch.setattr(main, "urlopen", probe)
    monkeypatch.setenv("PROMETHEUS_URL", "http://prometheus:9090")
    monkeypatch.setenv("GRAFANA_URL", "http://grafana:3000")
    status = TestClient(app).get("/api/platform-status").json()
    assert status["prometheus"] == "healthy"
    assert urls == ["http://prometheus:9090/-/ready", "http://grafana:3000/api/health"]


def test_public_monitoring_urls_use_selected_ports(monkeypatch):
    monkeypatch.setenv("PUBLIC_APP_PORT", "8012")
    monkeypatch.setenv("PUBLIC_PROMETHEUS_PORT", "9102")
    monkeypatch.setenv("PUBLIC_GRAFANA_PORT", "3012")
    status = TestClient(app).get("/api/platform-status").json()
    assert status["public_urls"] == {
        "application": "http://localhost:8012",
        "prometheus": "http://localhost:9102",
        "grafana": "http://localhost:3012",
    }
