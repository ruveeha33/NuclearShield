# NuclearShield

NuclearShield is a GitHub-ready implementation of an **Advanced Nuclear Facility Cybersecurity Platform with SCADA Protection, Safety System Integrity, and Nuclear Material Security for Civil and Defense Applications**. It demonstrates how a safety-preserving assurance platform can ingest passive evidence, identify explainable anomalies, correlate cyber/physical/material records, retain an audit trail, generate an HTML safeguards report, and expose health metrics to Prometheus and Grafana.

> **Safety boundary:** Every included record is fictional and labeled synthetic. NuclearShield cannot send commands and must never connect to a real nuclear, SCADA, I&C, safety, physical-access or material-accounting environment.

## What you can demonstrate

- A premium responsive dashboard with original floating facility artwork.
- Read-only CSV/JSON evidence ingestion with validation and SHA-256 provenance.
- Zeek/Suricata-style passive network records, integrity records, access events, MC&A/radiation evidence and change records.
- Five explainable detection paths: baseline rules, authorization checks, integrity validation, robust statistical anomaly scoring and actor/asset correlation.
- A detailed Sentrix-inspired in-browser HTML report covering what was detected, which evidence source detected it, the detection method, recommended measures, decision authority, compliance mapping and append-only demo audit records.
- Persistent multi-file history with dataset switching and dedicated Ingestion, Overview, SCADA, Integrity, Material, AI Detection, DevSecOps, Compliance, Reports, Monitoring and Audit views.
- Prometheus metrics and a provisioned Grafana dashboard with working local links.
- Editable Mermaid architecture, data-flow, workflow and security diagrams.
- Level 6 trade-offs, failure/recovery and oral-exam runbook.

## Fastest complete setup with Docker

Prerequisites: Git, Docker Desktop, Docker Compose, and free ports 8000, 9090 and 3000.

```powershell
git clone https://github.com/ruveeha33/NuclearShield.git
cd NuclearShield
Copy-Item .env.example .env
powershell -ExecutionPolicy Bypass -File .\\start-nuclearshield.ps1
```

On Windows, you can instead double-click `START-NUCLEARSHIELD.cmd`. It starts the
complete stack and opens the application without requiring a typed command.

The launcher rebuilds and recreates the containers, waits for the application
health check, and opens NuclearShield automatically. It reuses cached images and
downloads a monitoring image only on a computer where that image is missing.

If ports 8000, 9090 or 3000 are already occupied, the launcher selects the next
available ports automatically, saves them in `.runtime-ports.env`, updates the
application's monitoring links and prints the chosen ports in the terminal.

The launcher opens the web application automatically and prints all selected URLs.
With the preferred ports available, the addresses are:

- Web application: <http://localhost:8000>
- HTML report: <http://localhost:8000/api/report>
- Prometheus targets: <http://localhost:9090/targets>
- Prometheus prepared query: <http://localhost:9090/query?g0.expr=up%7Bjob%3D%22nuclearshield%22%7D&g0.show_tree=0&g0.tab=table>
- Grafana dashboard: <http://localhost:3000/d/nuclearshield/nuclearshield-evidence-assurance>

Grafana demo login defaults to `admin` / `nuclearshield-demo`. Change it in `.env` before using the stack outside a private local demonstration.

On the web application, open **Ingestion** and select **Analyze 24-row synthetic demonstration**. Prometheus begins collecting metrics automatically. The Grafana data source and twenty-panel dashboard are provisioned during startup. The Monitoring page includes direct links to targets, Grafana, raw metrics and prepared example queries.

The **Monitoring** page checks the actual Prometheus and Grafana service health from inside the Docker network. If either service is unavailable it reports that state instead of displaying a false success.

If an older Grafana image previously failed to download, run:

```powershell
docker compose down
docker compose pull grafana prometheus
docker compose up --build -d
docker compose ps
```

Stop the stack:

```powershell
docker compose down
```

Remove the local demo volumes only when you intentionally want to erase audit and monitoring data:

```powershell
docker compose down --volumes
```

## Run without Docker

This starts the website and API only. Prometheus and Grafana require the Docker path above.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
$env:NUCLEARSHIELD_DATA_DIR = "$PWD\data"
uvicorn app.main:app --reload
```

In another terminal:

```powershell
cd NuclearShield
.venv\Scripts\Activate.ps1
pytest -q
ruff check app tests
bandit -q -r app -x app/static
```

## Evidence schema

CSV and JSON files use a flexible adapter. It recognizes common alternatives for ID, timestamp, source, observed value, baseline, actor and asset, generates safe row IDs when absent, and infers one of six evidence domains where necessary. Optional authorization, integrity and signature fields enrich scoring. Every accepted and rejected row is counted. The demonstration limit is 10 MB and 50,000 records per file.

For the strongest analysis, provide `event_id`, `timestamp`, `event_type`, `source`, `value`, `baseline`, `authorized`, `integrity`, `actor` and `asset`. Robust peer-group anomaly scoring activates when an evidence domain contains at least five numeric records.

The analyzer treats declared evidence as untrusted input. It reports deviations; it does not assert that an event represents a real plant condition.

## Repository map

```text
app/                 FastAPI API, analyzer, audit store and responsive frontend
sample-data/         Fictional evidence used in the oral demonstration
monitoring/          Prometheus and provisioned Grafana configuration
docs/diagrams/       Editable Mermaid architecture, data-flow, workflow and security diagrams
docs/DEMO.md         End-to-end oral demonstration and failure/recovery sequence
docs/DECISIONS.md    Level 6 architecture rationale and trade-offs
tests/               Analyzer and API safety-boundary tests
.github/workflows/   Test, lint and static security-analysis gates
```

## Responsible AI disclosure

AI assisted with code, documentation and original artwork generation. The student remains responsible for understanding, validating and defending every design choice. The AI-assisted path uses transparent median/MAD peer-group anomaly detection, combines it with deterministic rules and correlations, and exposes confidence and contributors. It does not represent a validated nuclear ML model.

## Scope and limitations

This project maps evidence themes to IEC 62645, NRC RG 5.71 and IAEA guidance. It does not reproduce those standards, certify compliance, validate a physical data diode, implement a production SIEM, or replace qualified safety, safeguards, cyber or regulatory authorities.

Use [docs/REQUIREMENTS-MAP.md](docs/REQUIREMENTS-MAP.md) to trace requirements and [docs/DEMO.md](docs/DEMO.md) for the presentation walkthrough.
