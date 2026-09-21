# UI and Monitoring Update

- Restored the original compact navigation pattern and removed the separate Threat Center route.
- Threat detection, correlation, explanations and generated alerts now live inside AI Detection.
- Reworked the landing content below the hero into five compact capability cards plus a short evidence workflow.
- Removed the oversized dark evidence-lifecycle block.
- Removed transparent content-card styling; operational cards are opaque.
- SCADA now focuses on OT/network evidence, assets, baselines, anomalies and severity.
- Zeek-style and Suricata-style passive sensor evidence moved to Monitoring.
- Added `/api/network-monitoring`, which classifies latest uploaded network evidence into Zeek-style, Suricata-style and other passive evidence and links matching detections.
- Monitoring now includes dynamic Zeek/Suricata sensor workbenches, live record/detection/asset counts, recent sensor evidence, Prometheus/Grafana health and telemetry.
- Added more dynamic charts/statistics across SCADA, AI Detection and Monitoring.
- Existing report history/delete behavior and automatic port selection are preserved.
