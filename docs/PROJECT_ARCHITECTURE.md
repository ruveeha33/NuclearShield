# NuclearShield Project Architecture

## Purpose

NuclearShield is a safe, defensive, educational simulation for demonstrating nuclear-facility cybersecurity concepts. It does not connect to or control real nuclear, SCADA, PLC, safety-I&C, physical-access, or nuclear-material systems.

## Runtime flow

```text
Synthetic Facility Simulator
          |
          +--> FacilityState --> Rich Terminal Command Center
          |         |
          |         +--> Defensive Evidence Reporting
          |
          +--> Prometheus Metrics Endpoint (:9108)
                    |
                    v
              Prometheus (:9090)
                    |
                    v
                Grafana (:3000)
```

## Core components

### `src/nuclearshield/model.py`
Defines the synthetic facility state: illustrative plant signals, safety/instrumentation integrity, cyber-risk indicators, zone health, safeguards state, compliance evidence, and event history.

### `src/nuclearshield/simulator.py`
Generates bounded synthetic evidence for normal operation and classroom scenarios. It uses defensive anomaly scoring and risk fusion. Scenario logic changes simulated evidence only; it contains no exploit or control capability.

### `src/nuclearshield/dashboard.py`
Renders the NuclearShield terminal command center. Its major areas are the Protected Safety Envelope, Protection Rings, Command Assessment, Safeguards Watch, Assurance Board, and Security Operations Ticker.

### `src/nuclearshield/launcher.py`
Provides the professional workstation entry screen. It separates the full Command Workstation, terminal-only analysis, system diagnostics, and architecture/assurance views so the demonstration begins from a calm, deliberate operator interface rather than directly from a simulated event.

### `src/nuclearshield/metrics.py`
Publishes synthetic state as Prometheus gauges on port 9108. These metrics are read-only observability data for the local demonstration.

### `src/nuclearshield/reporting.py`
Turns the final synthetic state into an examiner-friendly defensive evidence summary. Optional exports are written as JSON and text under `reports/`.

### `src/nuclearshield/cli.py`
Coordinates the briefing, self-check, architecture view, monitoring stack startup, terminal session, reporting, and report export.

## Monitoring stack

`docker-compose.yml` starts two local visualization services:

- Prometheus collects NuclearShield's synthetic metrics.
- Grafana presents the facility-defense monitoring wall: facility protection overview, safety/I&C assurance, OT/SCADA cyber-defense posture, safeguards, assurance evidence, and protection-ring health.

The Docker services are monitoring-only and have no command path into the simulator.

## Defense-in-depth model

NuclearShield represents the following conceptual protection areas:

1. Enterprise / SOC
2. Industrial DMZ
3. OT / SCADA monitoring
4. Conceptual one-way evidence gateway
5. Independent Safety I&C assurance
6. Physical security / access analytics
7. Nuclear material accounting and control (MC&A)
8. Human review, audit, and compliance evidence

This is an educational architecture abstraction, not a real facility deployment design.

## Scenario model

- `normal` — nominal synthetic evidence.
- `scada-anomaly` — simulated OT anomaly/configuration-drift evidence.
- `safety-integrity` — simulated safety/instrumentation assurance concern.
- `insider-risk` — simulated physical-cyber access-risk correlation.
- `material-variance` — simulated MC&A reconciliation variance.
- `combined` — rotates through the classroom scenarios for the oral demonstration.

## AI role

The AI component is used for defensive anomaly detection on synthetic feature vectors. Its result is combined with deterministic safety, access, configuration, safeguards, and cyber-physical indicators to create an advisory risk level. Decisions remain human-review oriented; NuclearShield never issues plant-control actions.

## Evidence and compliance

The interface presents conceptual evidence mappings for IEC 62645, NRC RG 5.71, and IAEA guidance. These indicators demonstrate how monitoring evidence could support an assurance process; they are not certification claims.

The software assurance model uses review gates, automated tests, configuration-baseline checks, and evidence release. This is a practical educational approximation of assurance and change-control concepts; NuclearShield does not claim to implement formal mathematical verification of a real safety system.

The threat-context view is deliberately synthetic and high level. It demonstrates defensive correlation concepts but does not consume a live nuclear-sector indicator feed and does not contain exploit procedures.

## Civil and defense application context

For civil use cases, the architecture can represent cybersecurity assurance concepts for regulated power-generation or research environments: separation of enterprise and operational domains, independent safety assurance, safeguards, auditability, and controlled change.

For defense-oriented use cases, the same architecture is presented only at a governance level: strict separation, integrity monitoring, accountability, physical-cyber correlation, evidence retention, and human authorization for highly protected environments. No classified architecture, operational procedure, physical layout, or real security-control configuration is modeled.

## Conceptual implementation roadmap

1. Build and validate the synthetic baseline and classroom scenarios.
2. Add defensive analytics and cross-domain correlation using synthetic evidence.
3. Add read-only observability, audit/reporting, CI validation, and software-assurance gates.
4. Evaluate governance, validation, evidence retention, and organizational approval requirements before any real-world deployment discussion.

NuclearShield stops at the educational simulation and evaluation stage. The roadmap is not a procedure for connecting the project to a real facility.

## Safety boundary

NuclearShield deliberately excludes real-device discovery, industrial command execution, exploit chains, malware, credential theft, persistence, evasion, security bypass instructions, and destructive functions. All facility values, identities, events, anomalies, material variances, and decisions are synthetic.
