# NuclearShield

**Advanced Nuclear Facility Cybersecurity Platform — safe defensive educational simulation**

Current development status: **v1.0.0rc1 on `develop`**. The release candidate is not yet promoted to `main`.

NuclearShield is a terminal-first cybersecurity demonstration for an EduQual Level 6 AI Operations oral topic on nuclear-facility cybersecurity. It uses **synthetic data only** to demonstrate SCADA/OT protection, safety-system integrity, nuclear material safeguards, physical-cyber convergence, AI-assisted anomaly detection, compliance evidence, nuclear-software assurance concepts, and safety-preserving incident triage.

> **Safety boundary:** NuclearShield never connects to a real nuclear facility, reactor, PLC, SCADA network, safety instrument, physical-access system, radiation instrument, or nuclear material accounting system. It contains no exploit tooling, destructive industrial commands, credential theft, persistence, evasion, or bypass procedures.

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

That launches the briefing, combined synthetic scenario, terminal command center, Prometheus metrics, local Grafana/Prometheus monitoring stack, and an end-of-session evidence report.

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
| Exam Command Mode | complete rotating presentation scenario + browser monitoring + evidence export |
| Terminal Command | combined terminal-only facility defense simulation + summary report |
| SCADA Watch | synthetic OT/SCADA anomaly monitoring |
| Safety Watch | synthetic Safety-I&C integrity assurance |
| Safeguards Watch | MC&A / nuclear-material security evidence |
| Access Watch | insider-risk and physical-cyber correlation |
| Architecture | conceptual defense-in-depth explanation |
| System Self-Check | Python, Docker and project readiness checks |
| Assurance Gates | DevSecOps, configuration-control and evidence-gate model |
| Threat Context | safe, high-level nuclear-sector defensive context |

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

Run the full monitoring demonstration with a report and exported evidence:

```bash
python -m nuclearshield --briefing --monitoring --scenario combined --report --export-report
```

Run the local readiness check:

```bash
python -m nuclearshield --self-check
```

Show the nuclear-software assurance gates:

```bash
python -m nuclearshield --assurance
```

Show the safe defensive threat context:

```bash
python -m nuclearshield --threat-context
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

- **Facility Core / Safety Envelope** — synthetic plant telemetry, Safety-I&C integrity, instrumentation integrity, firmware integrity, and a disabled write path.
- **Protection Rings** — Enterprise/SOC, Industrial DMZ, OT/SCADA, Safety, physical security, and MC&A safeguards.
- **Command Assessment** — AI anomaly, configuration drift, insider/access risk, cyber-physical correlation, fused risk, and a human-review response posture.
- **Safeguards Watch** — synthetic material-accounting reconciliation, physical-security posture, access analytics, and safeguards status.
- **Assurance Board** — conceptual IEC 62645, NRC RG 5.71, and IAEA guidance mapping, compliance readiness, and audit coverage.
- **Security Operations Ticker** — live classroom-safe security and safeguards events.

## Grafana Facility Protection Command

Docker Compose provisions Prometheus and Grafana automatically. The Grafana dashboard is organized as a facility-protection board rather than a generic chart collection. It includes command status, safety envelope integrity, instrumentation integrity, cyber threat pressure, assurance readiness, firmware trust, MC&A variance, insider risk, cyber-physical correlation, plant/safety trends, safeguards evidence, and protection-ring health.

Prometheus collects only locally generated synthetic NuclearShield metrics.

## Defensive evidence reporting

Use `--report` to print an end-of-session examiner-friendly summary. Use `--export-report` to save both JSON and text evidence under `reports/`.

The report includes final risk, response posture, alert count, safety and instrumentation integrity, anomaly/configuration evidence, MC&A variance, access risk, compliance readiness, audit coverage, key findings, and the explicit synthetic-system safety boundary.

## Architecture and assurance views

```bash
python -m nuclearshield --architecture
python -m nuclearshield --assurance
python -m nuclearshield --threat-context
```

The architecture represents controlled monitoring paths, segmented trust zones, independent safety boundaries, physical-cyber correlation, safeguards evidence, and human review. The assurance view demonstrates a five-gate educational lifecycle model for approved change, automated verification, configuration control, safety-impact review, and evidence release. The threat-context view remains high-level and defensive and contains no exploit procedures or live attack feed.

These are **conceptual educational models**, not real nuclear deployment or certification blueprints.

## Exam-topic mapping

| Topic area | NuclearShield demonstration |
|---|---|
| Nuclear SCADA & I&C security | segmented protection rings, passive monitoring, conceptual one-way evidence path |
| Safety-system integrity | continuous synthetic instrumentation, firmware and safety-integrity assurance |
| Nuclear material security | MC&A reconciliation variance and safeguards review |
| Physical-cyber convergence | synthetic access risk correlated with cyber evidence |
| AI-driven threat detection | IsolationForest-assisted anomaly scoring plus multi-domain risk fusion |
| Nuclear-sector threat intelligence | safe defensive threat-context view; no live IOC or offensive feed |
| Automated incident response | simulated monitoring / human-review decisions only; no control actions |
| DevSecOps | assurance gates, packaging, tests, compile checks, JSON validation and GitHub Actions CI |
| Configuration/change control | approved-baseline and configuration-drift evidence model |
| Regulatory compliance | conceptual IEC 62645, NRC RG 5.71 and IAEA evidence mapping |
| Monitoring | terminal command center + Prometheus + provisioned Grafana dashboard |
| Audit/reporting | terminal evidence summary plus JSON/text export |

For a requirement-by-requirement mapping, see `docs/TOPIC_132_REQUIREMENTS_MATRIX.md`.

## Testing and validation

```bash
pytest -q
python -m compileall -q src
python -m json.tool monitoring/grafana/dashboards/nuclearshield.json
python -m nuclearshield --self-check
python -m nuclearshield --architecture
python -m nuclearshield --assurance
python -m nuclearshield --threat-context
python -m nuclearshield --scenario combined --samples 2 --refresh-rate 10 --windowed --report --export-report
```

GitHub Actions runs the release-candidate validation on Python 3.10 and 3.12. See `docs/RELEASE_CANDIDATE_CHECKLIST.md` for the promotion gate.

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

## Documentation

- `docs/EXAM_DEMO_GUIDE.md` — recommended oral-exam walkthrough.
- `docs/PROJECT_ARCHITECTURE.md` — implementation architecture and data flow.
- `docs/TOPIC_132_REQUIREMENTS_MATRIX.md` — official-topic coverage matrix.
- `docs/RELEASE_CANDIDATE_CHECKLIST.md` — automated and manual promotion gate.

## Repository workflow

Development remains on `develop`. Do not merge to `main` until review and approval.
