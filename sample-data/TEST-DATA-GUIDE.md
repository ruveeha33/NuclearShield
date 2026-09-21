# NuclearShield synthetic test-data guide

All files in this folder are fictional, educational and safe. They contain no real nuclear, SCADA, process, personnel or material telemetry.

| File | What it proves | Expected result |
|---|---|---|
| `01-full-platform-synthetic.csv` | All evidence domains, baseline rules, robust anomalies, integrity and authorization failures, actor/asset correlation | 19 accepted rows, 100% processing coverage, multiple critical/medium findings |
| `02-flexible-schema-synthetic.csv` | Alternative column-name normalization and AI-assisted peer-group anomaly detection | 8 accepted rows; `FLEX-006` activates the robust anomaly model |
| `03-clean-baseline-synthetic.csv` | Clean-data behavior without manufactured alerts | 7 accepted rows and zero findings |
| `04-json-safeguards-synthetic.json` | JSON ingestion, insider-risk, MC&A, radiation, change and safety-integrity evidence | 5 accepted rows and cross-domain correlated findings |
| `05-partial-quality-synthetic.json` | Automatic type inference, generated normalization and visible rejection handling | 3 accepted rows, 1 rejected empty row, 75% processing coverage |

## Recommended demonstration order

1. Upload `03-clean-baseline-synthetic.csv` and show that clean evidence produces no false alert.
2. Upload `02-flexible-schema-synthetic.csv` and open **Evidence** to show normalized alternative columns.
3. Open **AI Insights** and inspect `FLEX-006`.
4. Upload `04-json-safeguards-synthetic.json`, then open **Safeguards** and inspect its related events.
5. Upload `05-partial-quality-synthetic.json` and show one rejected row plus truthful 75% coverage.
6. Upload `01-full-platform-synthetic.csv` for the final Command, Detections, Integrity, Compliance, Report, Audit and Monitoring walkthrough.

Every upload remains selectable from the dataset selector. In Grafana, use a time range such as **Last 15 minutes** after uploading the files.
