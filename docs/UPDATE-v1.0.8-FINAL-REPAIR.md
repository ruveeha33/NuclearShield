# NuclearShield v1.0.8 Final Repair

- Restored Integrity and Material/Safeguards workspaces by restoring the shared domain statistics helper.
- Replaced side alert rails with full-width, vertically scrollable detailed alert streams directly below workspace statistics.
- Alert entries now expose evidence ID, confidence, engine, source/asset, reasons, contributors and related evidence with a review action.
- Preserved Material and AI Detection charts while changing only their alert presentation.
- Extended passive monitoring ingestion to CSV, JSON, JSONL/NDJSON (Suricata EVE-style) and Zeek ASCII `.log` files with `#fields` headers.
- Monitoring classifies Zeek and Suricata records dynamically and exposes protocol/source/destination context when available.
- Removed instructional feed placeholders; empty feeds now report only the observed state of the current analysis.
- Kept the approved Prometheus/Grafana monitoring and dynamic-port behavior.
- Report print/download actions now remain in normal document flow and cannot cover report content while scrolling; they remain hidden in print output.
- Existing defensive/read-only safety boundaries are unchanged.
