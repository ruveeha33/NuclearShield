from fastapi.testclient import TestClient

from app.intelligence import read_catalog, review_indicators
from app.main import app


def test_catalog_exact_match_only_and_no_autonomous_action(tmp_path, monkeypatch):
    monkeypatch.setenv("NUCLEARSHIELD_DATA_DIR", str(tmp_path))
    client = TestClient(app)
    raw = (b"event_id,event_type,source,src_ip,dest_ip,value,baseline\n"
           b"N1,network,fictional-zeek,192.0.2.4,198.51.100.2,5,5\n"
           b"N2,network,fictional-zeek,192.0.2.40,198.51.100.2,5,5\n")
    created = client.post("/api/ingest", files={"file": ("offline.csv", raw)}).json()
    catalog = b'{"indicators":[{"id":"T1","kind":"source_ip","value":"192.0.2.4"}]}'
    response = client.post(f"/api/indicator-review?analysis_id={created['analysis_id']}",
                           files={"file": ("training.json", catalog)})
    assert response.status_code == 200
    result = response.json()
    assert [m["event_id"] for m in result["matches"]] == ["N1"]
    assert result["autonomous_containment"] is False
    assert result["facility_connection"] is False
    assert len(result["review_steps"]) == 5


def test_indicator_catalog_rejects_invalid_input():
    import pytest

    with pytest.raises(ValueError, match="invalid IP"):
        read_catalog(b'{"indicators":[{"kind":"source_ip","value":"not an address"}]}')
    with pytest.raises(ValueError, match="supported kind"):
        read_catalog(b'{"indicators":[{"kind":"regex","value":".*"}]}')
    indicators = read_catalog(b'{"indicators":[{"kind":"signature","value":"TEST"}]}')
    assert review_indicators([{"event_id": "N", "event_type": "network", "signature": "TEST"}],
                             indicators)["matches"][0]["event_id"] == "N"
