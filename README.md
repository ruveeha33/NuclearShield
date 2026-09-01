# NuclearShield

**Advanced Nuclear Facility Cybersecurity Platform — safe defensive educational simulation**

NuclearShield is a terminal-first cybersecurity demonstration for Ruveeha Ashfaq's EduQual Level 6 AI Operations oral topic on nuclear-facility cybersecurity. It uses **synthetic data only** to demonstrate SCADA/OT protection, safety-system integrity, nuclear material safeguards, physical-cyber convergence, AI-driven anomaly detection, compliance evidence, and safety-preserving incident triage.

> **Safety boundary:** NuclearShield never connects to a real nuclear facility, reactor, PLC, SCADA network, safety instrument, PACS/access-control system, radiation instrument, or nuclear material accounting system. It contains no exploit tooling, destructive industrial commands, credential theft, persistence, evasion, or bypass procedures.

## What makes this build different

The terminal UX uses the same *presentation philosophy* as the AquaSentinel exam console—live fullscreen layout, process/architecture strip, multi-column SOC panels, risk meter, event feed and safety footer—but the NuclearShield domain model, wording, scenarios, metrics, dashboards and logic are independently designed for nuclear cybersecurity.

## Terminal SOC dashboard

The live console contains:

- **Defense-in-depth digital facility map:** Enterprise/SOC → Industrial DMZ → OT/SCADA → independent Safety I&C, plus Physical Security and MC&A safeguards.
- **Safety System Integrity:** synthetic reactor/safety telemetry, instrumentation integrity, firmware integrity.
- **OT / SCADA Protection:** passive zone health, conceptual one-way gateway status, anomaly score and configuration drift.
- **AI Risk Fusion & Decision:** combined network, access, configuration, material and cyber-physical risk with human-review decisions.
- **Nuclear Material & Physical-Cyber:** MC&A reconciliation variance, physical access risk and safeguards status.
- **Assurance Evidence:** IEC 62645, NRC RG 5.71 and IAEA guidance mapping indicators, audit coverage and compliance readiness.
- **Active Event Feed:** classroom-safe synthetic security/safeguards events.

## Full exam demo — Windows

Requirements: Python 3.10+ and Docker Desktop for Grafana/Prometheus.

Double-click:

```bat
NuclearShield.bat
```

Choose **Full Exam Demo** to launch the terminal SOC and automatically start/open:

- Grafana: `http://localhost:3000/d/nuclearshield-main`
- Prometheus: `http://localhost:9090`
- Prometheus metrics endpoint: `http://localhost:9108/metrics`

Grafana local demo login: `admin` / `nuclearshield`.

For a one-click exam run:

```bat
run_exam_demo.bat
```

## Scenario demonstrations

```bash
python -m nuclearshield --scenario normal
python -m nuclearshield --scenario scada-anomaly
python -m nuclearshield --scenario safety-integrity
python -m nuclearshield --scenario insider-risk
python -m nuclearshield --scenario material-variance
python -m nuclearshield --scenario combined
```

`combined` rotates through the classroom scenarios and is the recommended presentation mode.

## Monitoring stack

```bash
python -m nuclearshield --monitoring --scenario combined
```

Docker Compose provisions Prometheus and a NuclearShield Grafana dashboard. Grafana visualizes safety integrity, instrumentation integrity, reactor/safety signals, cyber-risk fusion, MC&A safeguards, compliance readiness, audit evidence, alerts and security-zone health.

## Architecture view

```bash
python -m nuclearshield --architecture
```

The architecture is a **conceptual educational model**, not a real nuclear deployment blueprint. The simulator represents controlled monitoring paths and independent safety boundaries without giving operational instructions for real facilities.

## Exam-topic mapping

| Topic area | NuclearShield demonstration |
|---|---|
| Nuclear SCADA & I&C security | segmented zone health, passive monitoring, conceptual one-way evidence path |
| Safety-system integrity | continuous synthetic instrumentation, firmware and safety-integrity assurance |
| Nuclear material security | MC&A reconciliation variance and safeguards review |
| Physical-cyber convergence | synthetic badge/session risk correlated with cyber evidence |
| AI-driven threat detection | IsolationForest-assisted anomaly scoring plus multi-domain risk fusion |
| Automated incident response | **simulated** human-review / enhanced-monitoring decisions; no control actions |
| DevSecOps | package metadata, tests, compile checks and GitHub Actions CI |
| Regulatory compliance | conceptual IEC 62645, NRC RG 5.71 and IAEA guidance mapping with audit evidence |
| Monitoring | live terminal SOC + Prometheus + provisioned Grafana dashboard |

## Testing

```bash
pytest -q
python -m compileall -q src
```

## Repository workflow

Development remains on `develop`. Do not merge to `main` until review and approval.
