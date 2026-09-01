# NuclearShield

**Advanced Nuclear Facility Cybersecurity Platform — safe educational simulation**

NuclearShield is a terminal-first defensive cybersecurity demonstration for an EduQual Level 6 AI Operations oral project. It models, with synthetic data only, a layered nuclear-facility security operations view covering SCADA/OT segmentation, safety-system integrity, material control & accounting (MC&A), physical-cyber access analytics, anomaly detection, compliance readiness, and safety-preserving incident response.

> **Safety boundary:** this project never connects to a real nuclear facility, reactor, PLC, SCADA network, radiation instrument, PACS system, or nuclear material system. It contains no exploit tooling or destructive industrial controls.

## What you see

- **Live terminal dashboard** built with Rich.
- Synthetic reactor/safety telemetry and zone health.
- AI-style anomaly detection using `IsolationForest` over generated telemetry.
- Simulated insider/access-risk and MC&A variance signals.
- Defense-in-depth and one-way/data-diode health indicators.
- Compliance-readiness indicator mapped conceptually to IEC 62645, NRC RG 5.71, and IAEA guidance.
- Prometheus metrics endpoint on `localhost:9108`.
- **Prometheus dashboard** at `http://localhost:9090`.
- **Provisioned Grafana dashboard** at `http://localhost:3000`.

## Quick start — Windows

Requirements: Python 3.10+ and, for the web dashboards, Docker Desktop.

```bat
run.bat
```

The script creates a virtual environment, installs dependencies, starts Prometheus + Grafana through Docker Compose, then launches the terminal dashboard. Your browser opens Grafana and Prometheus automatically.

Grafana login: `admin` / `nuclearshield` (local demo credentials only).

## Manual start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python -m nuclearshield --monitoring
```

Terminal-only mode:

```bash
python -m nuclearshield
```

## Architecture

```text
Synthetic Facility Simulator
        |
        +--> Safety / SCADA / MC&A / Access signals
        |             |
        |             +--> IsolationForest anomaly score
        |
        +--> Rich terminal SOC dashboard
        |
        +--> Prometheus metrics :9108
                       |
                       +--> Prometheus :9090
                                |
                                +--> Grafana :3000
```

The simulated security architecture represents separation between enterprise/monitoring, OT/SCADA, safety-critical systems, physical security, and a conceptual one-way data-transfer boundary. These are visualization and learning abstractions, not deployment instructions for real facilities.

## Exam-topic mapping

| Topic area | NuclearShield demonstration |
|---|---|
| Nuclear SCADA & I&C security | segmented zone status, defense-in-depth view, conceptual one-way gateway |
| Safety-system integrity | continuous synthetic integrity score and instrumentation deviation alerts |
| Nuclear material security | MC&A variance and physical-cyber access risk |
| AI-driven threat detection | IsolationForest anomaly scoring on synthetic telemetry |
| Automated response | simulated safety-preserving isolation messages only |
| DevSecOps | tests, packaging, CI workflow, controlled configuration |
| Regulatory compliance | readiness indicator and audit-oriented event stream |
| Monitoring | Prometheus metrics plus provisioned Grafana dashboard |

## Testing

```bash
pytest -q
```

## Repository workflow

Development happens on `develop`. Merge to `main` only after project review and approval.
