<div align="center">

<img src="app/static/assets/nuclearshield-logo.svg" alt="NuclearShield Logo" width="170">

# ☢️ NuclearShield

### Advanced Nuclear Cybersecurity Assurance Platform

**Defensive · Read-Only · Evidence-Driven · Explainable · Auditable**

**Version 1.0.8**

NuclearShield is a defensive cybersecurity assurance workstation that transforms passive security evidence into explainable findings, correlations, monitoring intelligence, reports, and auditable human decisions — without sending commands to operational technology.

<br>

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-E6522C)
![Grafana](https://img.shields.io/badge/Grafana-Visualization-F46800)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Release-v1.0.8-orange)

</div>

---

## 🛡️ Safety Authority

> **NuclearShield is a defensive, read-only educational demonstrator.**
>
> Every included record is fictional and synthetic.
>
> NuclearShield has **no plant-control capability** and must never be connected to a real nuclear facility, SCADA/I&C network, safety system, physical-access system, nuclear material-accounting system, or production operational environment.

### READ-ONLY BOUNDARY

**Observe → Verify → Analyze → Explain → Report**

**Human authority remains the final decision boundary.**

---

# 🚀 Quick Start

## Requirements

Before running NuclearShield, install:

- Git
- Docker Desktop
- Docker Compose v2
- Windows 10/11
- Modern web browser

Clone the repository:

```powershell
git clone https://github.com/ruveeha33/NuclearShield.git
cd NuclearShield
```

### Windows — Recommended

Double-click:

```text
START-NUCLEARSHIELD.cmd
```

Or run:

```powershell
powershell -ExecutionPolicy Bypass -File .\start-nuclearshield.ps1
```

The launcher automatically:

- checks Docker;
- starts Docker Desktop when available but not ready;
- validates Docker Compose;
- detects port conflicts;
- selects safe alternative ports when necessary;
- builds the NuclearShield application;
- starts Prometheus and Grafana;
- waits for application health;
- displays the active URLs; and
- opens NuclearShield in the browser.

No unrelated process is terminated just to reclaim a preferred port.

---

# 🔄 NuclearShield Workflow

NuclearShield follows an **evidence-to-decision** model.

```mermaid
flowchart LR
    A["📁 Evidence"] --> B["📥 Ingestion"]
    B --> C["✓ Validation"]
    C --> D["🔐 Provenance"]
    D --> E["⚙️ Analysis"]
    E --> F["🔗 Correlation"]
    F --> G["🔎 Explainable Findings"]
    G --> H["👤 Human Review"]
    H --> I["📄 Report"]
    H --> J["📜 Audit"]
    H --> K["📊 Monitoring"]
```

### Evidence → Analysis → Explanation → Human Decision

NuclearShield does not turn a detection directly into an operational action.

Instead, it preserves the separation between **machine-assisted analysis** and **human authority**.

---

# 🧠 How NuclearShield Works

```mermaid
flowchart LR
    E["Passive Evidence"] --> I["Ingest & Validate"]
    I --> P["SHA-256 Provenance"]
    P --> D["Detection Engine"]
    D --> C["Correlation"]
    C --> F["Explainable Findings"]
    F --> H["Human Review"]

    H --> R["Reports"]
    H --> A["Audit"]
    H --> M["Monitoring"]
```

Passive evidence may include:

```text
Network Evidence
Integrity Evidence
Access Evidence
Material Evidence
Radiation Evidence
Change Evidence
Zeek-Style Evidence
Suricata-Style Evidence
```

The analysis pipeline combines validation, normalization, provenance, deterministic checks, statistical analysis, correlation, and explanation before presenting results for human review.

---

# 🎯 What NuclearShield Does

NuclearShield turns passive defensive evidence into a structured assurance workflow.

It is designed to answer:

> **What happened?**

> **Which evidence supports it?**

> **Why was it detected?**

> **How confident is the analysis?**

> **What events are related?**

> **What should be reviewed next?**

> **Who retains decision authority?**

The platform focuses on **defensible evidence**, not autonomous operational response.

---

# 🏗️ Platform Architecture

```mermaid
flowchart LR
    U["Analyst"] --> UI["NuclearShield UI"]
    UI --> API["FastAPI"]

    API --> ING["Evidence Ingestion"]
    ING --> DET["Detection & Correlation"]
    DET --> EXP["Explainable Findings"]

    EXP --> REV["Human Review"]
    REV --> REP["Reports"]
    REV --> AUD["Audit"]

    API --> MET["Metrics"]
    MET --> PRO["Prometheus"]
    PRO --> GRA["Grafana"]
```

NuclearShield separates **evidence ingestion, analysis, human review, reporting, audit, and monitoring** while maintaining a read-only operational boundary.

---

# 📥 Evidence Ingestion

NuclearShield accepts passive defensive evidence in:

| Format | Support |
|---|---|
| CSV | ✅ |
| JSON | ✅ |
| JSONL | ✅ |
| NDJSON | ✅ |
| Zeek ASCII `.log` | ✅ |

Zeek `.log` evidence requires a `#fields` header.

The ingestion workflow is:

```text
Upload
   ↓
File Validation
   ↓
Schema Adaptation
   ↓
Normalization
   ↓
Record Validation
   ↓
SHA-256 Provenance
   ↓
Domain Classification
   ↓
Analysis
```

### Demonstration Limits

```text
Maximum file size : 10 MB
Maximum records   : 50,000
```

---

# 🧩 Flexible Evidence Schema

NuclearShield recognizes common field alternatives rather than requiring every source to use exactly the same schema.

For the strongest analysis, evidence can include:

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

Supported evidence domains include:

```text
network
integrity
access
material
radiation
change
```

Evidence is treated as **untrusted input**.

A finding represents an analytical result — not proof that a real-world nuclear or industrial event occurred.

---

# 🔎 Explainable Detection Engine

NuclearShield avoids unexplained alert generation.

A finding can contain:

```text
Event ID
Severity
Confidence
Detection Engine
Reasons
Contributors
Related Events
Human Authorization Requirement
```

The platform combines multiple defensive detection paths.

### Deterministic Rules

Known evidence conditions are evaluated through transparent logic.

### Authorization Checks

Evidence can be evaluated for declared authorization state.

### Integrity Validation

Integrity-related records can be checked for declared mismatches or validation failures.

### Robust Statistical Analysis

Where sufficient peer-group numeric evidence exists, NuclearShield can perform robust anomaly analysis.

Statistical analysis is used as **decision-support evidence**, not proof of malicious activity.

### Correlation

Related records can be associated through shared evidence characteristics such as actors, assets, and event relationships.

---

# 🌐 Zeek & Suricata Evidence

NuclearShield supports passive network-security evidence inspired by common Zeek and Suricata evidence formats.

### Zeek-Style Evidence

```text
sample-data/06-zeek-conn-synthetic.log
```

### Suricata-Style Evidence

```text
sample-data/07-suricata-eve-synthetic.jsonl
```

The Monitoring workspace presents evidence-driven sensor consoles.

These consoles do **not** claim to represent live nuclear-facility telemetry.

They display uploaded or synthetic defensive evidence only.

---

# 🖥️ NuclearShield Workspaces

## 📊 Overview

Provides the high-level assurance picture:

- analyzed evidence;
- finding counts;
- severity information;
- evidence-domain information;
- recent analyses; and
- platform status.

---

## 📥 Ingestion

The entry point for evidence analysis.

Users can:

- upload supported evidence;
- inspect ingestion results;
- use the built-in synthetic demonstration; and
- create a persistent analysis record.

---

## ⚙️ SCADA

Provides a defensive view of industrial-control-oriented evidence.

The workspace is **passive and read-only**.

It does not:

- write PLC logic;
- issue SCADA commands;
- modify set points;
- manipulate field devices; or
- control physical processes.

---

## 🔐 Integrity

Surfaces integrity-oriented evidence and associated detection results.

The purpose is to support review of declared integrity state rather than automatically change system configuration.

---

## ☢️ Material

Provides synthetic safeguards-oriented evidence views for educational analysis.

No real nuclear-material records are included.

---

## 🧠 AI Detection

Displays explainable findings and their analytical context.

The emphasis is:

**why the finding exists**, not simply that an alert was generated.

---

## 🛠️ DevSecOps

Represents software-assurance and quality-gate information associated with the NuclearShield development lifecycle.

The repository includes:

- automated tests;
- linting;
- static security analysis; and
- GitHub Actions CI.

---

## 📋 Compliance

Provides evidence-oriented framework mappings.

These mappings help demonstrate how collected evidence may be organized against assurance themes.

They are **not certification or compliance attestation**.

---

## 📄 Reports

Transforms analysis results into a structured assurance report.

Reports include:

- analysis context;
- findings;
- severity;
- confidence;
- evidence;
- detection method;
- related evidence;
- recommended measures;
- decision authority;
- evidence mapping; and
- audit-oriented context.

Reports can be:

- viewed in-browser;
- printed; or
- downloaded as HTML.

The downloaded report embeds NuclearShield branding for offline viewing.

---

## 📡 Monitoring

Provides platform and passive security-monitoring visibility through:

- Prometheus
- Grafana
- NuclearShield metrics
- Zeek-style evidence
- Suricata-style evidence
- platform health information

---

## 📜 Audit

Maintains traceable platform activity.

The audit system is designed so that deleting an analyzed-file record does not silently erase the associated audit history.

---

# 📊 Monitoring Architecture

```mermaid
flowchart LR
    NS["NuclearShield"] --> MET["/metrics"]
    MET --> PROM["Prometheus"]
    PROM --> GRAF["Grafana Dashboard"]

    NS --> HEALTH["Platform Health"]
    HEALTH --> PROM
    HEALTH --> GRAF
```

NuclearShield checks actual service health.

If Prometheus or Grafana is unavailable, the interface reports the service as unavailable rather than showing a false success state.

---

# 🌐 Default Services

When preferred ports are available:

| Service | URL |
|---|---|
| ☢️ NuclearShield | `http://localhost:8000` |
| 📄 Assurance Report | `http://localhost:8000/api/report` |
| 📊 Prometheus | `http://localhost:9090` |
| 🎯 Prometheus Targets | `http://localhost:9090/targets` |
| 📈 Grafana | `http://localhost:3000` |

If a preferred port is unavailable, the launcher selects another available port.

Selected ports are recorded in:

```text
.runtime-ports.env
```

---

# 🐳 Docker Architecture

The complete NuclearShield environment runs through Docker Compose as three connected services.

```mermaid
flowchart LR
    USER["Browser"] --> NS["☢️ NuclearShield<br/>FastAPI"]
    NS --> MET["Application Metrics"]
    MET --> PROM["📊 Prometheus"]
    PROM --> GRAF["📈 Grafana"]

    USER --> PROM
    USER --> GRAF
```

### Services

| Service | Purpose | Default Port |
|---|---|---:|
| **NuclearShield** | Evidence analysis and assurance interface | `8000` |
| **Prometheus** | Metrics collection and target monitoring | `9090` |
| **Grafana** | Monitoring dashboards and visualization | `3000` |

Start the complete stack:

```powershell
docker compose up --build -d
```

Check services:

```powershell
docker compose ps
```

View logs:

```powershell
docker compose logs -f
```

Stop:

```powershell
docker compose down
```

Remove demonstration volumes only when intentionally clearing persistent demo data:

```powershell
docker compose down --volumes
```

---

# 🔌 Intelligent Port Handling

The Windows launcher checks:

```text
8000 → NuclearShield
9090 → Prometheus
3000 → Grafana
```

If another application already owns one of these ports, NuclearShield does **not** kill that application.

Instead:

```text
Preferred Port
      ↓
Availability Check
      ↓
   Available?
   ↙       ↘
 Yes       No
  ↓         ↓
Use It   Find Free Port
             ↓
       Save Runtime Port
```

This allows NuclearShield to coexist with other local Docker and development environments.

---

# 🔁 DevSecOps Pipeline

```mermaid
flowchart LR
    CODE["Code Change"] --> GIT["GitHub"]
    GIT --> CI["GitHub Actions"]

    CI --> RUFF["Ruff"]
    CI --> BANDIT["Bandit"]
    CI --> TEST["Pytest"]

    RUFF --> GATE["Quality Gate"]
    BANDIT --> GATE
    TEST --> GATE

    GATE --> RELEASE["Review / Release"]
```

The CI workflow is stored in:

```text
.github/workflows/ci.yml
```

It provides automated testing, linting, and static security-analysis gates.

---

# 🧪 Testing

For local development testing with Python 3.12:

```powershell
py -3.12 -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project and development dependencies:

```powershell
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

Run automated tests:

```powershell
pytest -q
```

Run linting:

```powershell
ruff check app tests
```

Run static security analysis:

```powershell
bandit -q -r app -x app/static
```

---

# 📁 Repository Structure

```text
NuclearShield/
│
├── app/
│   ├── main.py
│   ├── analyzer.py
│   ├── store.py
│   │
│   └── static/
│       ├── app.js
│       ├── styles.css
│       ├── report.css
│       └── assets/
│
├── data/
│
├── docs/
│
├── monitoring/
│   ├── prometheus.yml
│   └── grafana/
│
├── sample-data/
│
├── scripts/
│
├── tests/
│
├── .github/
│   └── workflows/
│
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── START-NUCLEARSHIELD.cmd
├── start-nuclearshield.ps1
├── pyproject.toml
├── SECURITY.md
├── LICENSE
└── README.md
```

---

# 🔒 Security Model

NuclearShield intentionally excludes operational control capability.

### NuclearShield does not provide:

```text
✗ Plant-control commands
✗ PLC manipulation
✗ SCADA write operations
✗ Exploit logic
✗ Real nuclear facility credentials
✗ Real nuclear material records
✗ Production plant topology
✗ Real process set points
✗ Safety-system manipulation
```

### NuclearShield is designed around:

```text
✓ Passive evidence
✓ Read-only analysis
✓ Explainable findings
✓ Human authorization
✓ Auditability
✓ Defensive monitoring
✓ Synthetic demonstrations
```

See:

```text
SECURITY.md
```

for the repository's safe-use boundary.

---

# 📚 Standards & Compliance Scope

NuclearShield can organize evidence themes relevant to nuclear cybersecurity and assurance frameworks.

The project includes evidence-oriented mappings associated with areas such as:

- IEC 62645
- NRC RG 5.71
- IAEA cybersecurity guidance

These mappings are provided for **educational and demonstrative purposes**.

> **Framework mapping does not mean certification.**

NuclearShield does not certify compliance, provide regulatory approval, replace qualified assessment, or establish that a real nuclear facility satisfies a standard.

Real-world cybersecurity, safety, safeguards, and regulatory decisions remain the responsibility of qualified organizations and authorities.

---

# 🤖 Responsible AI Disclosure

AI tools assisted with portions of:

- code development;
- documentation;
- testing support; and
- original visual development.

NuclearShield's analytical behavior remains inspectable.

The platform exposes:

- deterministic rules;
- statistical methods;
- correlation logic;
- confidence;
- detection reasons; and
- contributing evidence.

The project does **not** represent a validated nuclear-sector machine-learning model.

AI-supported analysis does not replace human authority.

---

# ⚠️ Responsible Use

NuclearShield is intended for:

- cybersecurity education;
- defensive demonstrations;
- evidence-analysis demonstrations;
- DevSecOps demonstrations;
- academic presentations;
- assurance workflow research; and
- synthetic cybersecurity experimentation.

It must not be connected to operational nuclear or industrial-control environments.

All included demonstration evidence is synthetic.

---

# 📄 License

NuclearShield is released under the **MIT License**.

See:

```text
LICENSE
```

---

# 👤 Author

## Ruveeha Ashfaq

**Co-Founder — HR Presents**

Focused on defensive cybersecurity, DevOps, cloud, Linux, containerization, and evidence-driven security platforms.

---

<div align="center">

## ☢️ NuclearShield

### Evidence First. Human Authority Preserved.

**Defensive · Read-Only · Explainable · Auditable**

**v1.0.8**

</div>
