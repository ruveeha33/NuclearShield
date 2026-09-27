import hashlib
import json

from fastapi.testclient import TestClient

from app.main import app


def test_evidence_packet_is_analysis_scoped_and_has_verifiable_checksum(tmp_path, monkeypatch):
    monkeypatch.setenv("NUCLEARSHIELD_DATA_DIR", str(tmp_path))
    client = TestClient(app)
    raw = (b"event_id,event_type,source,asset,actor,value,baseline,authorized,integrity\n"
           b"A1,access,fictional-pacs,training-store,training-actor,1,1,false,valid\n"
           b"M1,material,fictional-mca,training-store,training-actor,8,10,true,valid\n")
    ids = [client.post("/api/ingest", files={"file": ("repeated.csv", raw)}).json()["analysis_id"]
           for _ in range(2)]
    assert ids[0] != ids[1]
    for analysis_id in ids:
        response = client.get("/api/compliance-packet?analysis_id=" + analysis_id)
        assert response.status_code == 200
        assert response.headers["content-disposition"].endswith('"nuclearshield-training-evidence-packet.json"')
        packet = response.json()
        assert packet["analysis"]["id"] == analysis_id
        assert packet["evidence_counts"]["material"] == 1
        assert packet["safeguards_review"]["declared_inventory_differences"][0]["difference"] == -2
        assert len(packet["audit_references"]) == 1
        assert "NOT FOR REGULATORY SUBMISSION" in packet["classification"]
        stripped = {k: v for k, v in packet.items() if k not in ("packet_sha256", "hash_scope")}
        actual = hashlib.sha256(json.dumps(stripped, sort_keys=True, separators=(",", ":"),
                                           ensure_ascii=False).encode()).hexdigest()
        assert actual == packet["packet_sha256"]
    assert client.get("/api/compliance-packet?analysis_id=missing").status_code == 404
