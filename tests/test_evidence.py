from __future__ import annotations

import csv
import json
from pathlib import Path

from nuclearshield.evidence import analyze_file, analyze_files, infer_domain


def _write_csv(path: Path, columns: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(columns)
        writer.writerows(rows)


def test_domain_inference_uses_schema_not_filename(tmp_path: Path) -> None:
    path = tmp_path / "anything.csv"
    _write_csv(
        path,
        ["timestamp", "badge_id", "access_result", "failed_attempts", "behavior_score"],
        [[f"2026-01-01T00:{i:02d}:00", f"U{i:03d}", "GRANTED", i % 3, float(i)] for i in range(30)],
    )
    analysis = analyze_file(path)
    assert analysis.domain == "ACCESS / IDENTITY"
    assert analysis.row_count == 30
    assert "failed_attempts" in analysis.numeric_columns
    assert analysis.timestamp_column == "timestamp"


def test_unknown_schema_is_not_forced_into_nuclear_domain(tmp_path: Path) -> None:
    path = tmp_path / "mystery.json"
    path.write_text(json.dumps([{"alpha": i, "beta": i * 2} for i in range(25)]), encoding="utf-8")
    analysis = analyze_file(path)
    assert analysis.domain == "GENERAL / UNKNOWN"
    assert analysis.analyzed_rows == 25


def test_multiple_files_are_analyzed_without_fixed_count_or_order(tmp_path: Path) -> None:
    first = tmp_path / "z.csv"
    second = tmp_path / "a.csv"
    _write_csv(first, ["time", "inventory_variance", "audit_complete"], [[i, i / 10, "YES"] for i in range(25)])
    _write_csv(second, ["time", "network_connections", "protocol_failures"], [[i, 100 + i, i % 2] for i in range(25)])
    package = analyze_files([first, second])
    assert len(package.datasets) == 2
    assert package.total_rows == 50
    assert {item.domain for item in package.datasets} == {"MC&A / SAFEGUARDS", "OT / SCADA"}


def test_infer_domain_has_safe_unknown_fallback() -> None:
    domain, confidence, _ = infer_domain(["foo", "bar", "baz"])
    assert domain == "GENERAL / UNKNOWN"
    assert confidence == 0.0
