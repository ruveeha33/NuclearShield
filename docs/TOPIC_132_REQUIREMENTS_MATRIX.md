# Topic 132 — Examiner Requirements Matrix

This matrix maps the official EduQual Topic 132 learning objectives to the safe NuclearShield educational implementation. It is an evidence map, not a claim of production nuclear certification.

| Official topic area | NuclearShield evidence | Demonstration status |
|---|---|---|
| Air-gapped / defense-in-depth architecture | Protection Rings, Industrial DMZ, conceptual one-way gateway, architecture mode | Demonstrated conceptually |
| Reactor protection / safety instrumentation anomaly detection | Synthetic telemetry, IsolationForest anomaly scoring, safety-integrity scenario | Demonstrated with synthetic data |
| Data diodes / unidirectional gateways | Read-only gateway health state and architecture view | Demonstrated conceptually; no real gateway |
| Preserve safety-system independence and reliability | Independent Safety I&C zone, no write/control path, safety-preserving response modes | Demonstrated |
| Continuous safety software / firmware integrity | Instrumentation, firmware and configuration-drift evidence | Demonstrated with synthetic integrity signals |
| IEC 62645 automation | Assurance Board and evidence report mapping | Educational evidence mapping only |
| Physical + cyber material safeguards | PACS/access, physical-security, cyber correlation and MC&A views | Demonstrated with synthetic data |
| MC&A security automation | Material-balance variance, reconciliation status, safeguards report | Demonstrated with synthetic data |
| Insider threat behavioral/access analytics | Insider-risk scenario and access-risk score | Demonstrated with synthetic data |
| ML anomaly detection | scikit-learn IsolationForest | Implemented |
| Nuclear-sector threat intelligence | Defensive threat-context catalog and scenario classification | Simulated educational context only |
| Safety-preserving incident response | Advisory response modes, human review, no automated plant action | Demonstrated safely |
| Secure development lifecycle | Git branching, tests, CI, package isolation, security boundary | Implemented for project software |
| Formal-method validation | Documented assurance gate and deterministic invariants | Educational approximation; not formal certification |
| Change/configuration control | develop/main workflow, configuration-drift monitoring, CI gates | Implemented at project level |
| Automated security testing | GitHub Actions tests, compile checks, dashboard validation, self-check | Implemented |
| NRC / IAEA / national compliance monitoring | Assurance score and evidence mappings | Educational mapping only; not regulatory certification |
| Safeguards / non-proliferation reporting | Defensive evidence report with MC&A/safeguards section | Demonstrated at educational level |
| Regulatory audit trails | Timestamped event evidence and exported JSON/text report | Demonstrated |
| Civil and defense applications | Shared-core application-context documentation | Demonstrated conceptually without classified details |

## Safety interpretation

The official brief uses verbs such as “deploy” and “configure.” NuclearShield interprets those objectives as a **safe educational simulation**. It does not deploy into, connect to, configure, or control a real nuclear facility, reactor, PLC, SCADA network, PACS, safety I&C system, material-accounting system, or data diode.

## Remaining limitations

NuclearShield does not claim production certification, regulatory approval, real formal verification, real threat-intelligence ingestion, real PACS integration, or real air-gap/data-diode hardware. Those capabilities are represented through synthetic evidence and architecture concepts appropriate to the oral-exam demonstration.
