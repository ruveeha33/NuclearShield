# NuclearShield

**Schema-Driven Nuclear Cyber Defense Evidence Analysis Workstation**

[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](https://github.com/HaziqBinAfzal/NuclearShield/releases/tag/v1.0.0)
[![CI](https://github.com/HaziqBinAfzal/NuclearShield/actions/workflows/ci.yml/badge.svg)](https://github.com/HaziqBinAfzal/NuclearShield/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Safety](https://img.shields.io/badge/mode-defensive%20%7C%20read--only-green)](#safety-boundary)

**Stable release: v1.0.0**

NuclearShield is a terminal-first defensive analysis platform for nuclear-facility cybersecurity evidence. It analyzes **operator-supplied local files** and presents evidence-driven findings across OT/SCADA security, safety-system integrity, nuclear-material safeguards, physical-access activity, anomaly detection, assurance, monitoring, and reporting.

> **Safety boundary:** NuclearShield never connects to a real nuclear facility, reactor, PLC, SCADA network, safety instrument, physical-access system, radiation instrument, or nuclear material accounting system. It contains no exploit tooling, destructive industrial commands, credential theft, persistence, evasion, or bypass procedures.

## What v1.0.0 provides

- Colored terminal **Nuclear Cyber Defense Command Center**.
- CSV, JSON, JSONL and XLSX evidence ingestion.
- Schema profiling and evidence-domain inference without fixed filenames.
- Dynamic numeric-feature discovery and AI-assisted anomaly analysis.
- Evidence-source prioritization, data-quality assessment and aggregate risk scoring.
- Prometheus evidence metrics and a provisioned Grafana Cyber Defense Command Center.
- JSON and TXT evidence-report export.
- Windows launcher with automatic virtual-environment/package setup.
- Read-only architecture with human-review posture and no industrial control path.

## Evidence-driven operating model

NuclearShield starts with no evidence loaded. It does not automatically create an incident, select a scenario, or fabricate findings.

```text
USER-SUPPLIED EVIDENCE
        ↓
INGESTION + VALIDATION
        ↓
SCHEMA PROFILING + DOMAIN INFERENCE
        ↓
FEATURE DISCOVERY + ANOMALY ANALYSIS
        ↓
CROSS-FILE RISK ASSESSMENT
        ↓
TERMINAL COMMAND CENTER
        ↓
PROMETHEUS + GRAFANA + REPORTING
        ↓
HUMAN REVIEW
```

The platform adapts to the files supplied. Unsupported or absent evidence domains are not invented.

## Quick start — Windows

### Requirements

- Windows 10/11
- Python 3.10+
- Docker Desktop when Grafana/Prometheus monitoring is required

Download the latest stable source from the [v1.0.0 release](https://github.com/HaziqBinAfzal/NuclearShield/releases/tag/v1.0.0), extract it, then double-click:

```bat
NuclearShield.bat
```

The launcher prepares the local Python environment when necessary and opens the NuclearShield workstation.

### Main operations

| Operation | Purpose |
|---|---|
| **1 — Load + Open Terminal Command Center** | Analyze selected evidence and display the terminal operations dashboard |
| **2 — Command Center + Grafana Monitoring** | Analyze evidence, display the command center, start Prometheus/Grafana and open Grafana |
| **3 — Open Grafana** | Open the local NuclearShield browser dashboard |
| **4 — Open Prometheus** | Open the local Prometheus query interface |
| **5 — Open Raw Metrics** | Inspect evidence metrics exported by the active session |
| **6 — System Diagnostics** | Check local analysis/monitoring prerequisites |
| **7 — Architecture & Assurance** | Review the defensive architecture and assurance posture |

When monitoring is active, keep the NuclearShield terminal open. Use the prompt in the terminal to stop the local evidence-metrics session and return to the launcher.

## Monitoring

| Service | Local address |
|---|---|
| Grafana | `http://localhost:3000/d/nuclearshield-main` |
| Prometheus | `http://localhost:9090` |
| Raw evidence metrics | `http://localhost:9108/metrics` |

Default local Grafana credentials:

```text
Username: admin
Password: nuclearshield
```

Grafana and Prometheus visualize metrics derived from the evidence package loaded in the active NuclearShield session. They provide monitoring/analysis views only and have no control path to industrial systems.

## Supported evidence

Supported input formats:

```text
.csv
.json
.jsonl
.xlsx
```

Evidence is classified from schema/content rather than filename. Current semantic domains include:

- **OT / SCADA** — telemetry, network observations, configuration state and integrity evidence.
- **Safety / Integrity** — safety-system, instrumentation, software and firmware integrity evidence.
- **MC&A / Safeguards** — material-accounting, inventory/reconciliation and safeguards evidence.
- **Access / Identity** — access events, identity/activity signals and physical-cyber evidence.
- **Compliance / Audit** — audit evidence, approved baselines and change-control evidence.
- **General / Unknown** — safe fallback when the supplied schema does not support a stronger classification.

The exact calculations and anomaly features are derived from usable data actually present in each supplied dataset.

## AI-assisted anomaly analysis

NuclearShield discovers suitable numeric features from the supplied evidence and applies defensive anomaly analysis when sufficient data exists. Model output is treated as **evidence requiring human review**, not proof of an attack or compromise.

The command center reports source-level anomaly pressure and model flags without claiming unsupported incidents.

## Reporting

NuclearShield can export local JSON and TXT analysis reports containing evidence-source summaries, inferred domains, record counts, discovered features, missing-data information, anomaly scores and human-review safety framing.

Reports are derived from the operator-supplied evidence package and do not create control instructions.

## Manual installation

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Launch the workstation:

```bash
python -m nuclearshield.launcher
```

Useful checks:

```bash
python -m nuclearshield --self-check
python -m nuclearshield --architecture
python -m nuclearshield --assurance
python -m nuclearshield --threat-context
```

## Testing and validation

```bash
pytest -q
python -m compileall -q src
python -m json.tool monitoring/grafana/dashboards/nuclearshield.json
python -m nuclearshield --self-check
```

GitHub Actions provides automated CI validation for repository changes.

## Clean shutdown

Windows:

```bat
stop.bat
```

Linux/macOS:

```bash
./stop.sh
```

## Safety boundary

NuclearShield is a **defensive, educational, read-only evidence analysis platform**.

It does **not**:

- connect to or control real nuclear facilities;
- connect to real SCADA, PLC, reactor-control or safety-I&C systems;
- issue industrial or physical-security control commands;
- provide exploit chains or security-bypass procedures;
- contain malware, credential theft, persistence or evasion tooling;
- claim that anomaly-model output proves a cyberattack.

All operational decisions remain outside the platform and require qualified human review.

## Documentation

- `docs/PROJECT_ARCHITECTURE.md` — implementation architecture and data flow.
- `docs/TOPIC_132_REQUIREMENTS_MATRIX.md` — project-scope coverage matrix.
- `docs/RELEASE_CANDIDATE_CHECKLIST.md` — historical release-validation checklist.

## Release

**NuclearShield v1.0.0** is the first stable release.

- [Release page](https://github.com/HaziqBinAfzal/NuclearShield/releases/tag/v1.0.0)
- [Source ZIP](https://github.com/HaziqBinAfzal/NuclearShield/archive/refs/tags/v1.0.0.zip)

Future development should be performed on `develop` or feature branches and validated before promotion to `main`.