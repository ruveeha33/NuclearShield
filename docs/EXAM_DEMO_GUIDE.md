# NuclearShield Exam Demonstration Guide

This guide is for the safe educational presentation of NuclearShield. All telemetry, events, identities, access records, safety values, material-accounting signals, and cyber anomalies are synthetic.

## Recommended live sequence

1. Run `NuclearShield.bat` or `run_exam_demo.bat` to open the NuclearShield workstation entry screen.
2. Start with **System Diagnostics** and explain that the project checks its local demonstration prerequisites before a session.
3. Open **Architecture & Assurance** and explain the defense-in-depth model: Enterprise / SOC, Industrial DMZ, OT / SCADA monitoring, an independent Safety I&C assurance boundary, physical-security monitoring, MC&A safeguards, and human review.
4. Explain the assurance gates: change review, automated verification, configuration control, safety-impact review, and evidence release. These are educational software-assurance concepts, not certification claims.
5. Launch **Command Workstation**. The terminal command center is the operator-facing view, while Grafana is the monitoring-wall view. Prometheus supplies the local observability metrics.
6. Point to the **Protected Safety Envelope** and explain that it represents synthetic safety and instrumentation evidence rather than plant control.
7. Explain the **Protection Rings**: Enterprise, DMZ, OT-SCADA, Safety, Physical, and MC&A. Their purpose is to demonstrate separation of critical functions and defense in depth.
8. Use **Command Assessment** to explain anomaly scoring, configuration drift, access risk, cyber-physical correlation, and why elevated conditions lead to human review instead of autonomous action.
9. Use **Safeguards Watch** to explain material control and accounting (MC&A), physical-security evidence, access analytics, and reconciliation.
10. Show the **Security Operations Ticker** as the audit-oriented event stream, then switch to Grafana to show the same synthetic evidence over time.
11. End the terminal session with `Ctrl+C`. Show the defensive evidence report and the JSON/text files written under `reports/` when export is enabled.
12. Run `stop.bat` after the demonstration to stop the local monitoring stack.

## Scenario choices

- `combined`: rotating presentation scenario covering several domains.
- `scada-anomaly`: synthetic OT/SCADA anomaly and segmentation evidence.
- `safety-integrity`: synthetic safety-I&C and instrumentation-integrity degradation.
- `material-variance`: synthetic MC&A reconciliation anomaly.
- `insider-risk`: synthetic physical-access and insider-risk correlation.
- `normal`: baseline monitoring state.

## Civil and defense application context

NuclearShield uses one defensive monitoring concept for two high-level contexts. In a civil context, the presentation can describe regulated power-generation or research facilities where cyber monitoring, independent safety assurance, safeguards, audit evidence, and controlled change management are important. In a defense context, the same principles can be described at a non-operational level for highly protected or regulated facilities where confidentiality, integrity, availability, physical security, material accountability, and strict human authorization are especially important.

The project deliberately does not model classified procedures, real facility layouts, operational security processes, or any control capability. The civil/defense comparison is conceptual and governance-focused.

## Implementation roadmap

**Phase 1 — Synthetic baseline:** define the facility state model, safe classroom scenarios, terminal visualization, and reporting.

**Phase 2 — Defensive analytics:** add anomaly scoring, cross-domain correlation, configuration-drift evidence, access-risk evidence, and safeguards reconciliation using synthetic data.

**Phase 3 — Observability and assurance:** expose read-only metrics to Prometheus, visualize them in Grafana, add CI validation, configuration-control evidence, and human-review gates.

**Phase 4 — Regulated-environment evaluation:** conceptually evaluate governance, assurance, evidence retention, validation, and organizational approval requirements before any real-world deployment discussion. NuclearShield itself remains a simulation and does not provide a real deployment procedure.

## Useful commands

```text
python -m nuclearshield --self-check
python -m nuclearshield --architecture
python -m nuclearshield --assurance
python -m nuclearshield --threat-context
python -m nuclearshield --briefing --scenario combined
python -m nuclearshield --briefing --monitoring --scenario combined --report --export-report
```

## Examiner-safe explanation

NuclearShield is not a reactor-control product and is not a deployment guide for a real facility. It is an educational digital monitoring simulation showing how cybersecurity, safety integrity, physical security, safeguards, AI-assisted anomaly detection, observability, software assurance, audit evidence, and human review can be presented together in a defense-in-depth architecture.
