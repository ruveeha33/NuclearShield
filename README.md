# ☢️ NuclearShield

> **Advanced Nuclear Facility Cybersecurity Platform with SCADA Protection, Safety System Integrity, and Nuclear Material Security for Civil and Defense Applications**

NuclearShield is a defensive, read-only, evidence-driven cybersecurity assurance workstation designed to demonstrate how passive evidence can be ingested, validated, analyzed, correlated, monitored, and reported without sending commands to operational technology.

> ⚠️ **Safety Boundary**  
> Every included record is fictional and labeled synthetic. NuclearShield must never be connected to a real nuclear, SCADA, I&C, safety, physical-access, or material-accounting environment.

---

##  What NuclearShield Demonstrates

- Read-only CSV and JSON evidence ingestion
- SHA-256 provenance and evidence validation
- Zeek/Suricata-style passive network evidence
- SCADA and industrial-control evidence views
- Integrity and authorization checks
- Explainable statistical anomaly detection
- Actor, asset, and time-window correlation
- Material and radiation evidence handling
- Detailed in-browser safeguards reports
- Prometheus metrics
- Provisioned Grafana monitoring dashboard
- Append-only demonstration audit records
- Docker-based reproducible deployment
- CI/CD and static security-analysis workflow
- Editable architecture and workflow diagrams

---

## 🚀 Quick Start — Windows + Docker

### 1️⃣ Prerequisites

Install:

- Git
- Docker Desktop
- Docker Compose

Make sure **Docker Desktop is running** before starting NuclearShield.

Default host ports:

| Service | Default Port |
|---|---:|
| NuclearShield | `8000` |
| Prometheus | `9090` |
| Grafana | `3000` |

The ports can be changed in `.env` if another local application already uses them.

---

### 2️⃣ Clone NuclearShield

Open **PowerShell**:

```powershell
cd $HOME\Documents
git clone https://github.com/ruveeha33/NuclearShield.git
cd NuclearShield
```

If you already cloned the repository:

```powershell
cd $HOME\Documents\NuclearShield
git pull origin main
```

If your clone is stored somewhere else, simply `cd` into that NuclearShield directory.

---

### 3️⃣ Create the Local Environment File

```powershell
Copy-Item .env.example .env
```

The default configuration includes:

```env
APP_PORT=8000
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

GRAFANA_ADMIN_USER=admin
GRAFANA_ADMIN_PASSWORD=nuclearshield-demo
```

If port `8000`, `9090`, or `3000` is already being used, edit `.env` and assign a different host port.

Example:

```env
APP_PORT=8001
PROMETHEUS_PORT=9091
GRAFANA_PORT=3001
```

---

### 4️⃣ Start NuclearShield

Run:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-nuclearshield.ps1
```

The launcher:

1. Checks that Docker is installed.
2. Verifies that the Docker Engine is running.
3. Creates `.env` from `.env.example` when necessary.
4. Reads the configured host ports.
5. Checks those ports for conflicts.
6. Reports the owning Windows process or Docker container when possible.
7. Starts NuclearShield, Prometheus, and Grafana.
8. Waits for the NuclearShield API health check.
9. Opens NuclearShield automatically in your browser.

Normal launcher startup uses cached images with `--pull never`.

---

## 🌐 Open the Services

With the default ports:

| Service | Address |
|---|---|
| NuclearShield | `http://localhost:8000` |
| HTML Report | `http://localhost:8000/api/report` |
| Prometheus | `http://localhost:9090` |
| Prometheus Targets | `http://localhost:9090/targets` |
| Grafana | `http://localhost:3000` |

Grafana demonstration login:

```text
Username: admin
Password: nuclearshield-demo
```

Change the Grafana password in `.env` before using the stack outside a private local demonstration.

---

## 🧪 Run the Synthetic Demonstration

After NuclearShield opens:

1. Open **Ingestion**.
2. Select **Analyze 24-row synthetic demonstration**.
3. Allow the evidence pipeline to process the dataset.
4. Review the Overview and domain-specific evidence views.
5. Open **AI Detection** for explainable anomaly results.
6. Open **Reports** for detailed detection evidence.
7. Open **Monitoring** for Prometheus and Grafana access.
8. Open **Audit** for demonstration traceability.

Prometheus collects metrics automatically after the stack is running.

The Grafana data source and NuclearShield dashboard are provisioned during startup.

---

## 🧯 Port Conflict Troubleshooting

To see the running containers:

```powershell
docker ps
```

To inspect the NuclearShield Compose stack:

```powershell
docker compose ps
```

To identify a Windows process using port `8000`:

```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen
```

For Prometheus:

```powershell
Get-NetTCPConnection -LocalPort 9090 -State Listen
```

For Grafana:

```powershell
Get-NetTCPConnection -LocalPort 3000 -State Listen
```

If another legitimate application needs the port, do **not** terminate it unnecessarily. Change the corresponding port in `.env` instead.

---

## 🐳 Docker Commands

### Check container status

```powershell
docker compose ps
```

### View logs

```powershell
docker compose logs
```

### Follow logs live

```powershell
docker compose logs -f
```

### Stop NuclearShield

```powershell
docker compose down
```

### Start again

```powershell
powershell -ExecutionPolicy Bypass -File .\start-nuclearshield.ps1
```

### Rebuild manually

```powershell
docker compose up --build --pull never --force-recreate -d
```

---

## 📥 Prometheus / Grafana Image Recovery

If the required Prometheus or Grafana image is not available locally:

```powershell
docker compose down
docker compose pull grafana prometheus
docker compose up --build -d
docker compose ps
```

This intentionally downloads the required monitoring images.

---

## 🗑️ Reset Local Demonstration Data

Only run this when you intentionally want to remove the Docker volumes containing local demonstration and monitoring data:

```powershell
docker compose down --volumes
```

---

## 🐍 Run Without Docker

This starts the NuclearShield website/API directly. Prometheus and Grafana still require the Docker deployment path.

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
$env:NUCLEARSHIELD_DATA_DIR = "$PWD\data"
uvicorn app.main:app --reload
```

Open:

```text
http://localhost:8000
```

---

## 🧪 Development Checks

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Run tests:

```powershell
pytest -q
```

Run Ruff:

```powershell
ruff check app tests
```

Run Bandit:

```powershell
bandit -q -r app -x app/static
```

---

## 🔄 Evidence Workflow

```text
Synthetic CSV / JSON Evidence
            │
            ▼
      Evidence Ingestion
            │
            ▼
   Validation + Provenance
            │
            ▼
   Domain Classification
            │
            ▼
 ┌─────────────────────────┐
 │ Deterministic Rules     │
 │ Authorization Checks    │
 │ Integrity Validation    │
 │ Statistical Detection   │
 │ Evidence Correlation    │
 └─────────────────────────┘
            │
            ▼
   Explainable Findings
            │
      ┌─────┴─────┐
      ▼           ▼
   Reports     Monitoring
                 │
           ┌─────┴─────┐
           ▼           ▼
       Prometheus    Grafana
```

---

## 🧠 Detection Approach

NuclearShield uses explainable detection paths including:

- Baseline deviation rules
- Authorization validation
- Integrity checks
- Robust peer-group statistical anomaly scoring
- Actor/asset correlation

The AI-assisted analysis path uses transparent statistical methods such as median/MAD peer-group anomaly detection together with deterministic rules and correlations.

NuclearShield reports **evidence deviations**. It does not claim that a detected event represents an actual nuclear-plant condition.

---

## 📂 Evidence Schema

CSV and JSON evidence can include fields such as:

```text
event_id
timestamp
event_type
source
value
baseline
authorized
integrity
actor
asset
```

The adapter recognizes common field alternatives and can infer evidence domains where appropriate.

Every accepted and rejected row is counted.

Demonstration limits:

- Maximum file size: **10 MB**
- Maximum records per file: **50,000**

---

## 🏗️ Repository Structure

```text
NuclearShield/
│
├── app/                  # FastAPI application, analyzer and frontend
├── sample-data/          # Fictional synthetic demonstration evidence
├── monitoring/           # Prometheus and Grafana configuration
├── docs/                 # Project documentation and diagrams
├── tests/                # Analyzer and API safety-boundary tests
├── .github/workflows/    # CI/CD and security-analysis gates
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── start-nuclearshield.ps1
└── README.md
```

---

## 🔐 Security Design

The Docker deployment applies defensive restrictions to the NuclearShield application container, including:

- Read-only container filesystem
- Dedicated persistent evidence volume
- Temporary `/tmp` filesystem
- `no-new-privileges`
- Dropped Linux capabilities
- Non-root application user
- Application health checks
- Synthetic evidence boundary
- No operational control capability

NuclearShield is designed for **demonstration, education, evidence analysis, and defensive assurance** — not plant operation.

---

## 📊 Monitoring

Prometheus collects NuclearShield health and application metrics.

Grafana provides the provisioned monitoring dashboard.

The NuclearShield **Monitoring** page checks the actual service health of Prometheus and Grafana from inside the Docker network rather than displaying a static success state.

---

## 📑 Reports

NuclearShield provides a detailed HTML safeguards report containing:

- Executive summary
- Detection results
- Evidence source
- Detection methodology
- Record-level evidence
- Correlation information
- SHA-256 provenance
- Recommended defensive measures
- Decision authority
- Compliance mapping
- Audit traceability
- Safety and methodology limitations

---

## ⚠️ Responsible Use

NuclearShield is a defensive educational and assurance platform.

It must **not** be used to:

- Control nuclear equipment
- Send commands to SCADA/PLC/I&C systems
- Modify safety systems
- Operate physical-access systems
- Operate material-accounting systems
- Represent synthetic evidence as real plant telemetry

All included demonstration evidence is fictional and synthetic.

---

## 📚 Standards & Scope

The project maps evidence themes to areas discussed in:

- IEC 62645
- NRC Regulatory Guide 5.71
- IAEA cybersecurity guidance

This project does **not** claim regulatory certification or compliance and does not replace qualified safety, safeguards, cybersecurity, or regulatory authorities.

---

## 🤖 Responsible AI Disclosure

AI assisted with parts of the code, documentation, and original visual development.

The student remains responsible for understanding, validating, presenting, and defending the project's design decisions.

The AI-assisted detection path is intended to remain transparent and explainable rather than acting as an autonomous nuclear decision system.

---
