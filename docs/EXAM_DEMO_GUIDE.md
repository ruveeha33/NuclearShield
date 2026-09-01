# NuclearShield Exam Demonstration Guide

This guide is for the safe educational presentation of NuclearShield. All telemetry, events, identities, access records, safety values, material-accounting signals, and cyber anomalies are synthetic.

## Recommended live sequence

1. Run `NuclearShield.bat` and choose **EXAM COMMAND MODE**.
2. Use the pre-mission briefing to explain that the platform is defensive, read-only, and disconnected from real nuclear or OT systems.
3. Point to the **Facility Core / Safety Envelope** and explain that it represents synthetic reactor and safety-I&C evidence rather than reactor control.
4. Explain the **Protection Rings**: Enterprise, DMZ, OT-SCADA, Safety, PACS, and MC&A. Their purpose is to demonstrate defense-in-depth and separation of critical functions.
5. Use **Command Assessment** to explain anomaly scoring, configuration drift, access risk, cyber-physical correlation, and why a high score results in human review rather than autonomous control.
6. Use **Safeguards Watch** to explain material control and accounting (MC&A), physical security, access analytics, and reconciliation.
7. Use **Assurance Board** to show how the demo records conceptual evidence mapping for IEC 62645, NRC RG 5.71, and IAEA guidance.
8. Show the **Security Operations Ticker** as the audit-oriented event stream.
9. Open Grafana to show historical/time-series observability, then Prometheus to explain where the local metrics come from.
10. End by stating that NuclearShield performs no real PLC, SCADA, PACS, safety-system, reactor, or nuclear-material control action.

## Scenario choices

- `combined`: rotating presentation scenario covering several domains.
- `scada-anomaly`: synthetic OT/SCADA anomaly and segmentation evidence.
- `safety-integrity`: synthetic safety-I&C and instrumentation-integrity degradation.
- `material-variance`: synthetic MC&A reconciliation anomaly.
- `insider-risk`: synthetic physical-access and insider-risk correlation.
- `normal`: baseline monitoring state.

## Useful commands

```text
python -m nuclearshield --self-check
python -m nuclearshield --architecture
python -m nuclearshield --briefing --scenario combined
python -m nuclearshield --briefing --monitoring --scenario combined
```

## Examiner-safe explanation

NuclearShield is not a reactor-control product and is not a deployment guide for a real facility. It is an educational digital monitoring simulation showing how cybersecurity, safety integrity, physical security, safeguards, AI-assisted anomaly detection, observability, audit evidence, and human review can be presented together in a defense-in-depth architecture.
