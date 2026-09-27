from pathlib import Path

from app.analyzer import analyze, network_model, parse_evidence


def test_csv_parsing_and_anomaly_explanation():
    raw = b"event_id,timestamp,event_type,source,value,baseline,authorized,integrity\nE1,2026-01-01T00:00:00Z,integrity,sensor,b,a,false,mismatch\n"
    events, rejected = parse_evidence("evidence.csv", raw)
    findings = analyze(events)
    assert rejected == []
    assert len(findings) == 1
    assert findings[0].score == 100
    assert findings[0].requires_human_authorization is True


def test_rejects_unsupported_type():
    raw = b"event_id,timestamp,event_type,source,value,baseline\nE1,t,command,x,1,1\n"
    try:
        events, _ = parse_evidence("evidence.csv", raw)
        assert events[0]["event_type"] == "network"
    except ValueError as exc:
        raise AssertionError("flexible schema should normalize unknown classes") from exc


def test_flexible_schema_and_robust_outlier():
    rows = ["id,time,sensor,reading,expected,category"]
    rows += [
        f"N{i},2026-01-01T00:00:0{i}Z,zeek,{v},10,network"
        for i, v in enumerate([9, 10, 10, 11, 10, 90])
    ]
    events, rejected = parse_evidence("flex.csv", ("\n".join(rows)).encode())
    findings = analyze(events)
    assert not rejected
    assert len(events) == 6
    assert any("robust-anomaly-model" in finding.engine for finding in findings)


def test_network_isolation_forest_uses_uploaded_values_and_explains_outlier():
    raw = (Path(__file__).resolve().parents[1] / "sample-data" / "isolation-forest-network-synthetic.csv").read_bytes()
    events, _ = parse_evidence("synthetic.csv", raw)
    result = network_model(events)
    assert result["status"] == "completed"
    assert result["eligible_rows"] == 40
    assert result["features"] == ["value", "duration"]
    assert any(row["event_id"] == "SYN-NET-037" for row in result["outliers"])
    findings = analyze(events, result)
    assert any(f.event_id == "SYN-NET-037" and "isolation-forest" in f.engine for f in findings)
    assert all(f.requires_human_authorization for f in findings)


def test_network_model_reports_insufficient_data_without_fabrication():
    events, _ = parse_evidence("few.csv", b"event_id,event_type,value\nA,network,1\nB,network,200\n")
    result = network_model(events)
    assert result["status"] == "insufficient_data"
    assert result["outliers"] == []
    assert not any("isolation-forest" in finding.engine for finding in analyze(events, result))
