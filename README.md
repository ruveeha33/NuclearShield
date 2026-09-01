# NuclearShield

**Advanced Nuclear Facility Cybersecurity Platform — safe defensive educational simulation**

NuclearShield is a terminal-first cybersecurity demonstration for an EduQual Level 6 AI Operations oral topic on nuclear-facility cybersecurity. It uses **synthetic data only** to demonstrate SCADA/OT protection, safety-system integrity, nuclear material safeguards, physical-cyber convergence, AI-assisted anomaly detection, compliance evidence, and safety-preserving incident triage.

> **Safety boundary:** NuclearShield never connects to a real nuclear facility, reactor, PLC, SCADA network, safety instrument, PACS/access-control system, radiation instrument, or nuclear material accounting system. It contains no exploit tooling, destructive industrial commands, credential theft, persistence, evasion, or bypass procedures.

## NuclearShield experience

The project is designed as a distinct **facility-protection command console** rather than a generic monitoring screen. The terminal centers on the synthetic facility core and safety envelope, protection rings, command assessment, safeguards watch, assurance evidence, and a live security-operations ticker.

The browser monitoring layer uses Prometheus plus a provisioned Grafana **Facility Protection Command** dashboard for safety, OT/SCADA, cyber-risk, safeguards, audit, and defense-in-depth evidence.

## Fastest exam start — Windows

Requirements:

- Windows 10/11
- Python 3.10+
- Docker Desktop only if Grafana and Prometheus are required

From the project folder, double-click:

```bat
NuclearShield.bat
```

Recommended exam option:

```text
[1] EXAM COMMAND MODE
```

That launches the briefing, combined synthetic scenario, terminal command center, Prometheus metrics, and the local Grafana/Prometheus monitoring stack.

Grafana: `http://localhost:3000/d/nuclearshield-main`

Prometheus: `http://localhost:9090`

Metrics: `http://localhost:9108/metrics`

Grafana demo login: `admin` / `nuclearshield`

A direct one-click exam launcher is also available:

```bat
run_exam_demo.bat
```

## Command modes

| Launcher mode | Demonstrates |
|---|---|
| Exam Command Mode | complete rotating presentation scenario + browser monitoring |
| Terminal Command | combined terminal-only facility defense simulation |
| SCADA Watch | synthetic OT/SCADA anomaly monitoring |
| Safety Watch | synthetic Safety-I&C integrity assurance |
| Safeguards Watch | MC&A / nuclear-material security evidence |
| Access Watch | insider-risk and physical-cyber correlation |
| Architecture | conceptual defense-in-depth explanation |
| System Self-Check | Python, package, Docker and project readiness checks |

## Manual start

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Run a terminal-only demonstration:

```bash
python -m nuclearshield --briefing --scenario combined
```

Run the full monitoring demonstration:

```bash
python -m nuclearshield --briefing --monitoring --scenario combined
```

Run the local readiness check:

```bash
python -m nuclearshield --self-check
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

`combined` rotates through the classroom scenarios and is the recommended oral-presentation mode.

## Terminal command center

The live command console presents:

- **Facility Core / Safety Envelope** — synthetic plant telemetry, Safety-I&C integrity, instrumentation integrity, firmware integrity, and locked write-path status.
- **Protection Rings** — Enterprise/SOC, Industrial DMZ, OT/SCADA, Safety, PACS/physical security, and MC&A safeguards.
- **Command Assessment** — AI anomaly, configuration drift, insider/access risk, cyber-physical correlation, fused mission risk, and a human-review disposition.
- **Safeguards Watch** — synthetic material-accounting reconciliation, physical-security posture, access analytics, and safeguards status.
- **Assurance Board** — conceptual IEC 62645, NRC RG 5.71, and IAEA guidance evidence mapping, compliance readiness, and audit coverage.
- **Security Operations Ticker** — live classroom-safe security and safeguards events.

## Grafana Facility Protection Command

Docker Compose provisions Prometheus and Grafana automatically. The Grafana dashboard is organized as a facility-protection board rather than a generic chart collection. It includes command status, safety envelope integrity, instrumentation integrity, cyber threat pressure, assurance readiness, firmware trust, MC&A variance, insider risk, cyber-physical correlation, plant/safety trends, safeguards evidence, and complete protection-ring health.

Prometheus collects only locally generated synthetic NuclearShield metrics.

## Architecture

```bash
python -m nuclearshield --architecture
```

The architecture represents controlled monitoring paths, segmented trust zones, independent safety boundaries, physical-cyber correlation, safeguards evidence, and human review. It is a **conceptual educational model**, not a real nuclear deployment blueprint.

## Exam-topic mapping

| Topic area | NuclearShield demonstration |
|---|---|
| Nuclear SCADA & I&C security | segmented protection rings, passive monitoring, conceptual one-way evidence path |
| Safety-system integrity | continuous synthetic instrumentation, firmware and safety-integrity assurance |
| Nuclear material security | MC&A reconciliation variance and safeguards review |
| Physical-cyber convergence | synthetic access risk correlated with cyber evidence |
| AI-driven threat detection | IsolationForest-assisted anomaly scoring plus multi-domain risk fusion |
| Automated incident response | simulated monitoring / human-review decisions only; no control actions |
| DevSecOps | packaging, tests, compile checks, JSON validation and GitHub Actions CI |
| Regulatory compliance | conceptual IEC 62645, NRC RG 5.71 and IAEA evidence mapping |
| Monitoring | terminal command center + Prometheus + provisioned Grafana dashboard |

## Testing and validation

```bash
pytest -q
python -m compileall -q src
python -m json.tool monitoring/grafana/dashboards/nuclearshield.json
python -m nuclearshield --self-check
```

GitHub Actions tests supported Python versions and validates the Grafana dashboard JSON.

## Clean shutdown

Exit the terminal with `Ctrl+C`.

To stop Grafana and Prometheus on Windows:

```bat
stop.bat
```

On Linux/macOS:

```bash
./stop.sh
```

## Troubleshooting

If the terminal runs but the browser dashboards do not, verify Docker Desktop is running and use **System Self-Check** from `NuclearShield.bat`.

If port `3000`, `9090`, or `9108` is already occupied, stop the conflicting local service before restarting the demo.

If Python dependencies are missing, rerun `NuclearShield.bat` or reinstall with `pip install -r requirements.txt` inside the project virtual environment.

## Presentation guide

See `docs/EXAM_DEMO_GUIDE.md` for the recommended oral-exam walkthrough and explanation sequence.

## Repository workflow

Development remains on `develop`. Do not merge to `main` until review and approval.
