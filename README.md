# NuclearShield

**Advanced Nuclear Facility Cybersecurity Analysis Platform — defensive, read-only, file-driven**

Current development status: **v1.0.0rc1 on `develop`**. The release candidate is not yet promoted to `main`.

NuclearShield is a terminal-first defensive analysis platform for nuclear-facility cybersecurity evidence. It is designed to analyze **operator-supplied local files only** and correlate evidence across OT/SCADA security, safety-system integrity, nuclear-material safeguards, physical-access activity, anomaly detection, assurance, and reporting.

> **Safety boundary:** NuclearShield never connects to a real nuclear facility, reactor, PLC, SCADA network, safety instrument, physical-access system, radiation instrument, or nuclear material accounting system. It contains no exploit tooling, destructive industrial commands, credential theft, persistence, evasion, or bypass procedures.

## Data-first operating model

NuclearShield starts with no evidence loaded. It does not automatically create an incident, select a scenario, or populate the workstation with generated findings.

The intended workflow is:

```text
Operator supplies files
        ↓
Evidence intake and validation
        ↓
Per-file identification and domain classification
        ↓
Domain-specific analysis
        ↓
Cross-domain correlation
        ↓
Terminal workstation + Prometheus/Grafana + evidence report
```

A typical evidence package can contain separate files for OT/SCADA telemetry, Safety I&C integrity, MC&A/safeguards data, and physical-access/insider-risk events. NuclearShield will report what each file contains and keep its findings traceable to the supplied source file.

## Windows start

Requirements:

- Windows 10/11
- Python 3.10+
- Docker Desktop only when Grafana and Prometheus are required

From the project folder, double-click:

```bat
NuclearShield.bat
```

The workstation opens in an empty state showing **NO DATA LOADED** and **WAITING FOR INPUT**. Analysis begins only after evidence files are supplied.

Grafana: `http://localhost:3000/d/nuclearshield-main`

Prometheus: `http://localhost:9090`

Metrics: `http://localhost:9108/metrics`

Grafana local login: `admin` / `nuclearshield`

## Workstation operations

| Operation | Purpose |
|---|---|
| Load Evidence Package | inspect and analyze operator-supplied files |
| System Diagnostics | verify the local analysis environment |
| Architecture & Assurance | review the defensive analysis and assurance model |

The evidence intake workflow is being finalized around the actual datasets supplied to the project. This prevents hard-coding assumptions about filenames, columns, schemas, or record meanings before the source data is known.

## Manual installation

Create and activate a virtual environment, then install the package:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

Run the workstation:

```bash
python -m nuclearshield.launcher
```

Run the local readiness check:

```bash
python -m nuclearshield --self-check
```

Show the defensive architecture and software-assurance views:

```bash
python -m nuclearshield --architecture
python -m nuclearshield --assurance
python -m nuclearshield --threat-context
```

## Analysis domains

NuclearShield is structured around the following evidence domains:

- **OT / SCADA** — telemetry, network observations, configuration state, and integrity evidence.
- **Safety I&C** — safety-system, instrumentation, software, and firmware integrity evidence.
- **Nuclear safeguards / MC&A** — material-accounting, inventory/reconciliation, and safeguards evidence.
- **Physical access / insider risk** — access events, identity/activity signals, and physical-cyber correlation.
- **Assurance / compliance** — audit evidence, approved baselines, change control, and conceptual standards mapping.

The exact calculations, charts, and anomaly features are derived from the supplied datasets rather than fabricated when data is absent.

## Terminal command center

Once an evidence package is loaded, the command console is intended to present:

- source-file identity and record counts;
- evidence-domain classification;
- Safety I&C and instrumentation findings;
- OT/SCADA anomaly and configuration findings;
- safeguards/MC&A reconciliation findings;
- physical-access and insider-risk findings;
- cross-domain correlation and human-review posture;
- evidence provenance and event timeline.

No control commands are generated or sent to industrial systems.

## Browser monitoring

Docker Compose provisions Prometheus and Grafana locally. The Grafana Facility Cyber Defense board visualizes metrics derived from the active evidence package. It is a monitoring and analysis surface only and has no control path back to any industrial or physical system.

## Defensive evidence reporting

Reports are designed to remain traceable to the files supplied by the operator. Findings should identify the source file/domain, calculated evidence, resulting advisory assessment, and safety boundary. JSON/text export remains available for local evidence summaries.

## Architecture and assurance

The architecture represents segmented monitoring, independent safety boundaries, physical-cyber correlation, safeguards evidence, auditability, and human review. Assurance views describe approved change, automated verification, configuration control, safety-impact review, and evidence release.

These are conceptual defensive models, not real nuclear deployment or certification blueprints.

## Project-scope mapping

| Topic area | NuclearShield capability |
|---|---|
| Nuclear SCADA & I&C security | file-driven OT/SCADA evidence analysis and segmented monitoring model |
| Safety-system integrity | Safety I&C, instrumentation, software and firmware evidence analysis |
| Nuclear material security | MC&A and safeguards evidence analysis |
| Physical-cyber convergence | access/identity evidence correlated with cyber and safeguards findings |
| AI-driven threat detection | anomaly scoring over suitable features present in supplied data |
| Nuclear-sector threat context | defensive interpretation only; no offensive feed or exploit procedure |
| Incident response | advisory and human-review oriented; no industrial control actions |
| DevSecOps | tests, CI, configuration control and assurance evidence model |
| Regulatory compliance | conceptual IEC 62645, NRC RG 5.71 and IAEA evidence mapping |
| Monitoring | terminal command center + Prometheus + Grafana |
| Audit/reporting | source-traceable evidence summary and local exports |

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
```

## Clean shutdown

To stop local Grafana and Prometheus on Windows:

```bat
stop.bat
```

On Linux/macOS:

```bash
./stop.sh
```

## Documentation

- `docs/PROJECT_ARCHITECTURE.md` — implementation architecture and data flow.
- `docs/TOPIC_132_REQUIREMENTS_MATRIX.md` — scope coverage matrix.
- `docs/RELEASE_CANDIDATE_CHECKLIST.md` — release validation gate.

## Repository workflow

Development remains on `develop`. Do not merge to `main` until review and approval.
