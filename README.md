# NuclearShield


**Schema-Driven Nuclear Cyber Defense Evidence Analysis Workstation**


[![Release](https://img.shields.io/badge/release-v1.0.0-blue)](https://github.com/ruveeha33/NuclearShield/releases/tag/v1.0.0)
[![CI](https://github.com/ruveeha33/NuclearShield/actions/workflows/ci.yml/badge.svg)](https://github.com/ruveeha33/NuclearShield/actions/workflows/ci.yml)
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
