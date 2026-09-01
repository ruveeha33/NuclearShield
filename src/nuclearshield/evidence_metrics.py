from __future__ import annotations

import re
import time
from dataclasses import dataclass

from prometheus_client import Gauge, start_http_server

from .evidence import EvidencePackage


def _slug(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return value[:80] or "unknown"


@dataclass
class EvidenceMetrics:
    files: Gauge
    rows: Gauge
    overall_risk: Gauge
    dataset_rows: Gauge
    dataset_missing: Gauge
    dataset_anomaly: Gauge
    dataset_flags: Gauge
    feature_value: Gauge


def create_metrics() -> EvidenceMetrics:
    return EvidenceMetrics(
        files=Gauge("nuclearshield_evidence_files", "Number of supplied evidence files"),
        rows=Gauge("nuclearshield_evidence_rows", "Total records indexed from supplied evidence"),
        overall_risk=Gauge("nuclearshield_evidence_risk_score", "Cross-file evidence anomaly pressure, 0-100"),
        dataset_rows=Gauge("nuclearshield_dataset_rows", "Rows in an evidence dataset", ["file", "domain"]),
        dataset_missing=Gauge("nuclearshield_dataset_missing_pct", "Missing-cell percentage", ["file", "domain"]),
        dataset_anomaly=Gauge("nuclearshield_dataset_anomaly_score", "Dataset anomaly pressure, 0-100", ["file", "domain"]),
        dataset_flags=Gauge("nuclearshield_dataset_anomaly_flags", "Rows flagged by the anomaly model", ["file", "domain"]),
        feature_value=Gauge("nuclearshield_feature_latest_value", "Latest numeric value observed in supplied evidence", ["file", "domain", "feature"]),
    )


def publish_package(package: EvidencePackage, metrics: EvidenceMetrics) -> None:
    metrics.files.set(len(package.datasets))
    metrics.rows.set(package.total_rows)
    metrics.overall_risk.set(package.overall_risk_score)
    for dataset in package.datasets:
        labels = {"file": dataset.filename, "domain": dataset.domain}
        metrics.dataset_rows.labels(**labels).set(dataset.row_count)
        metrics.dataset_missing.labels(**labels).set(dataset.missing_pct)
        metrics.dataset_anomaly.labels(**labels).set(dataset.anomaly_score)
        metrics.dataset_flags.labels(**labels).set(dataset.anomaly_count)
        if dataset.rows:
            latest = dataset.rows[-1]
            for feature in dataset.usable_features:
                try:
                    value = float(str(latest.get(feature, "")).replace(",", "").rstrip("%"))
                except (TypeError, ValueError):
                    continue
                metrics.feature_value.labels(file=dataset.filename, domain=dataset.domain, feature=_slug(feature)).set(value)


def serve_package(package: EvidencePackage, port: int = 9108) -> None:
    metrics = create_metrics()
    publish_package(package, metrics)
    start_http_server(port)
    while True:
        time.sleep(3600)
