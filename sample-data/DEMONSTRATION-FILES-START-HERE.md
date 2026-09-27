# NuclearShield oral-exam demonstration sequence

All evidence and indicators here are fictional training data. Extract the ZIP, run START-NUCLEARSHIELD.cmd, and upload evidence files via Ingestion. The indicator catalog has a separate Assurance Lab form.

1. Upload `NuclearShield-Full-Platform-100-Records.jsonl`: 100 records across six evidence types. Review Overview, SCADA, AI Detection, Material and Monitoring.
2. In Assurance Lab, inspect the bounded gateway/review policies and offline PACS/MC&A joins. Click `Run training catalog` to match a fictional documentation source IP to the uploaded network events. The catalog is not verified intelligence; matches are not confirmed attacks and require human review.
3. In Compliance or Reports, download `Evidence packet JSON`. It contains selected-run evidence counts, findings, safeguards review and audit references plus a checksum. It is NOT a regulatory submission or compliance certification.
4. Upload `08-later-integrity-snapshot.csv`. Assurance Lab shows a change for fictional `training-controller` across retained uploads; this is repeated offline review, not continuous facility monitoring.
5. Upload `NuclearShield-IsolationForest-80-Network-Records.csv` and open AI Detection for 80 scored network observations and model outliers. Reports keeps the earlier runs.

No plant interface, physical data diode, live PACS/MC&A connection, validated formal safety-code verification, autonomous containment or regulator submission is implemented. Prometheus/Grafana observe the application when Docker services are running. Qualified people authorize any real-world response outside NuclearShield.
