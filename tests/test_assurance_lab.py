from fastapi.testclient import TestClient

from app.assurance import check_change_review_policy, check_gateway_policy, gateway_allows
from app.main import app


def test_gateway_model_exhaustively_rejects_inbound_and_control():
    result = check_gateway_policy()
    assert result["states_checked"] == 48
    assert result["outbound_evidence_paths"] == 3
    assert result["status"] == "pass"
    assert not result["inbound_or_control_allowed"]
    assert gateway_allows("safety-replica", "analytics", "evidence")
    assert not gateway_allows("analytics", "safety-replica", "command")
    assert not gateway_allows("pacs-export", "analytics", "configuration")
    review = check_change_review_policy()
    assert review["status"] == "pass"
    assert review["states_checked"] == 16
    assert review["review_ready_states"] == 1


def test_offline_joins_and_snapshot_drift_survive_repeated_uploads(tmp_path, monkeypatch):
    monkeypatch.setenv("NUCLEARSHIELD_DATA_DIR", str(tmp_path))
    client = TestClient(app)
    first = b"event_id,event_type,source,asset,actor,value,baseline,authorized,integrity\nI1,integrity,replica,training-safety,,approved,approved,true,valid\nA1,access,pacs-export,training-store,casey,1,1,false,valid\nM1,material,mca-export,training-store,casey,8,10,true,valid\n"
    second = b"event_id,event_type,source,asset,actor,value,baseline,authorized,integrity\nI2,integrity,replica,training-safety,,changed,approved,true,mismatch\n"
    one = client.post("/api/ingest", files={"file": ("snapshot-one.csv", first)}).json()
    two = client.post("/api/ingest", files={"file": ("snapshot-two.csv", second)}).json()
    response = client.get(f"/api/assurance-lab?analysis_id={one['analysis_id']}")
    assert response.status_code == 200
    body = response.json()
    assert body["read_only"] and not body["live_facility_connection"]
    assert body["safeguards"]["matched_records"][0]["access_id"] == "A1"
    assert body["safeguards"]["inventory_differences"][0]["difference"] == -2
    assert body["integrity"]["changed_observations"][0]["current"]["event_id"] == "I2"
    assert body["integrity"]["changed_observations"][0]["current"]["analysis_id"] == two["analysis_id"]
    assert client.get("/api/assurance-lab?analysis_id=not-found").status_code == 404
