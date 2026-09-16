# NuclearShield requirements map

| Requirement | Implementation evidence |
|---|---|
| Air gap and defense in depth | Five-zone UI and `architecture.mmd`; evidence-only upload boundary |
| Passive Zeek/Suricata-style ingestion | Allowlisted network evidence records, synthetic sensor sources and the dynamic `SCADA Protection` page (`#/scada`) |
| Anomaly detection | Explainable baseline, authorization, integrity and robust median/MAD scoring shown under `AI Threat Detection` |
| Data diode concepts | One-way safety evidence path in UI and architecture diagram |
| Safety-system integrity | Firmware/configuration baseline mismatch scenario and data-driven `Safety Integrity` page |
| IEC 62645, NRC RG 5.71, IAEA | Framework mapping API/UI and explicit non-certification disclaimer |
| Physical-cyber, MC&A, insider risk | Access, material and radiation event types; correlated findings under `Material Security` |
| Governed AI/ML and threat context | Human/safety authorization on every finding, offline intelligence-context demonstration and no response endpoint |
| DevSecOps and change control | Tests, lint/security CI, non-root container, change evidence type and dynamic `Nuclear DevSecOps` page |
| Audit and safeguards reporting | SQLite audit entries and detailed Sentrix-inspired HTML report with detection source, method, measures, governance and framework mapping |
| Prometheus/Grafana | Metrics endpoint, scrape config, provisioned data source/dashboard |
| Architecture/network/data flow/workflow/security diagrams | Editable Mermaid sources in `docs/diagrams` |
| End-to-end demonstration | `DEMO.md` and included evidence dataset |
| Failure and recovery | Container stop/start scenario in the runbook |
| Trade-offs and governance | `DECISIONS.md`, authorization workflow and limitations |
