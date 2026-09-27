# NuclearShield 20-minute oral demonstration

Allow about 9 minutes for the slides, 9.5 minutes for the live platform, and 1.5 minutes for transitions. Extract the ZIP first, start Docker Desktop, and double-click `START-NUCLEARSHIELD.cmd` from the extracted folder. Run `powershell -ExecutionPolicy Bypass -File .\scripts\pre-exam-check.ps1` before presenting. The launcher may select different free ports; use the URLs it prints.

## Live sequence

| Time | Action | Explain |
| --- | --- | --- |
| 0:00–1:00 | Open the landing page and Ingestion. | Fictional, read-only evidence enters an assurance workstation; no OT control connection exists. |
| 1:00–2:30 | Upload `sample-data/NuclearShield-Full-Platform-100-Records.jsonl`. Open Overview and SCADA. | Show accepted records, SHA-256 provenance and explainable network findings. |
| 2:30–3:30 | Open Integrity and Material. | Discuss safety integrity, offline access/material joins and human review of safeguards evidence. |
| 3:30–4:45 | Open Assurance Lab, use Policy & evidence, and run the included training indicator catalog. | Show bounded gateway/review checks and fictional indicator matches; these are not verified threat intelligence or autonomous containment. |
| 4:45–6:00 | Open Compliance and Reports, then use Assurance Lab → Audit history; download the evidence packet JSON. | Show traceable references, framework mappings and retained uploads. The packet is not a regulatory submission or certification. |
| 6:00–7:00 | Upload `sample-data/08-later-integrity-snapshot.csv` and inspect Assurance Lab. | Show one changed fictional asset across offline uploads; this is not continuous plant monitoring. |
| 7:00–8:30 | Upload `sample-data/NuclearShield-IsolationForest-80-Network-Records.csv` and open AI Detection. | scikit-learn Isolation Forest scores uploaded network observations, flags outliers for review and cannot order plant actions. |
| 8:30–9:30 | Open Monitoring, Prometheus and Grafana via the displayed local links. | Application metrics and dashboards observe this demonstration stack; the ports may differ on the exam machine. |

The full-platform file should accept 100 records, produce findings, and complete Isolation Forest scoring for suitable network evidence. The focused ML file contains 80 network observations. Counts can depend on the selected upload and analysis state; show the actual interface results rather than promising an exact number of alerts.

## Interview boundaries

- The data diode is an architectural concept here, not physical diode hardware. No commands return to safety systems.
- PACS and MC&A joins operate on offline synthetic records, not live facility integrations.
- Scores and indicator matches are leads for an authorized human reviewer, not confirmed attacks or automated response.
- Regulatory mapping and audit references support a classroom demonstration; they do not establish IEC, NRC or IAEA certification.
- A production deployment would require validated operational data, independent safety review, approved architecture and site-specific authority.
