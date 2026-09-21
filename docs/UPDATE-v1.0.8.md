# NuclearShield v1.0.8 UI and workspace update

This update preserves the defensive, read-only evidence boundary while improving workspace separation and presentation.

- Landing hero image and primary copy preserved. Lower landing content redesigned into six mission-specific capability cards and a four-stage evidence lifecycle.
- Operational workspaces now always load the newest completed analysis. Historical runs are isolated in Reports & Analysis History.
- Reports retain Open, Print, Download HTML and Delete controls. Deletion retains an audit record.
- Added Threat Center with cross-domain severity, correlation, detection-method activity, alert cards and evidence queue.
- AI Detection now generates evidence-derived review alerts showing how and why each alert triggered.
- Integrity now has dedicated integrity metrics, state visualization, detection workflow, alerts and findings.
- Material/Safeguards now separates access, MC&A/material and radiation evidence and explains correlation logic.
- SCADA now surfaces Zeek-style, Suricata-style and other passive network evidence counts dynamically from the newest dataset.
- DevSecOps remains scoped to change/integrity evidence and regulated CI/change-control assurance.
- No autonomous control, containment, plant write-back, or fabricated live telemetry was added.

## Automatic port collision recovery
The Windows launcher now treats 8000/9090/3000 as preferred starting ports, not fixed requirements. It checks Windows listeners, Docker-published ports, and an OS bind test. If a port is occupied, it selects the next free port. If a race-condition collision still occurs while Docker publishes the port, the launcher cleans up only NuclearShield's partial Compose containers and retries with a new port set (up to 20 attempts). It never stops or removes the unrelated process/container that owns the occupied port.
