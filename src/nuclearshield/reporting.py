from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

from rich import box
from rich.panel import Panel
from rich.table import Table

from .model import FacilityState


def build_report(state: FacilityState) -> dict:
    """Build a safe, examiner-friendly summary from synthetic state only."""
    findings: list[str] = []
    if state.network_anomaly_score >= 0.35:
        findings.append("Elevated synthetic network anomaly evidence observed.")
    if state.configuration_drift_score >= 0.30:
        findings.append("Synthetic configuration-drift evidence requires review.")
    if state.access_risk_score >= 0.30:
        findings.append("Synthetic physical-cyber access risk requires human review.")
    if not state.material_accounting_ok:
        findings.append("Synthetic MC&A reconciliation variance requires safeguards review.")
    if state.safety_integrity_pct < 98 or state.instrumentation_integrity_pct < 98:
        findings.append("Synthetic safety/instrumentation integrity evidence requires assurance review.")
    if not findings:
        findings.append("No material synthetic security exception is active at report time.")

    return {
        "report": "NuclearShield Defensive Evidence Summary",
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "classification": "EDUCATIONAL SIMULATION / SYNTHETIC DATA",
        "scenario": state.scenario,
        "risk_level": state.risk_level,
        "response_mode": state.response_mode,
        "active_alerts": state.active_alerts,
        "safety_assurance": {
            "safety_integrity_percent": round(state.safety_integrity_pct, 2),
            "instrumentation_integrity_percent": round(state.instrumentation_integrity_pct, 2),
            "firmware_integrity_percent": round(state.firmware_integrity_pct, 2),
            "safety_zone_healthy": state.safety_zone_ok,
        },
        "cyber_defense": {
            "network_anomaly_percent": round(state.network_anomaly_score * 100, 2),
            "configuration_drift_percent": round(state.configuration_drift_score * 100, 2),
            "one_way_gateway_healthy": state.data_diode_ok,
            "scada_zone_healthy": state.scada_zone_ok,
        },
        "safeguards": {
            "material_balance_variance": round(state.material_balance_delta, 4),
            "material_accounting_healthy": state.material_accounting_ok,
            "physical_security_healthy": state.physical_security_ok,
            "access_risk_percent": round(state.access_risk_score * 100, 2),
            "cyber_physical_correlation_percent": round(state.cyber_physical_correlation * 100, 2),
        },
        "assurance": {
            "compliance_readiness_percent": round(state.compliance_score_pct, 2),
            "audit_evidence_coverage_percent": round(state.audit_coverage_pct, 2),
            "conceptual_mappings": ["IEC 62645", "NRC RG 5.71", "IAEA guidance"],
        },
        "findings": findings,
        "recent_events": list(state.event_log[:7]),
        "safety_boundary": "No real nuclear, SCADA, PLC, PACS, safety-I&C, or material-accounting system was connected or controlled.",
    }


def report_panel(state: FacilityState) -> Panel:
    report = build_report(state)
    table = Table.grid(expand=True, padding=(0, 1))
    table.add_column(style="bold cyan", width=22)
    table.add_column()
    table.add_row("SCENARIO", str(report["scenario"]).upper())
    table.add_row("FINAL RISK", str(report["risk_level"]))
    table.add_row("DECISION", str(report["response_mode"]))
    table.add_row("ACTIVE ALERTS", str(report["active_alerts"]))
    table.add_row("SAFETY INTEGRITY", f"{state.safety_integrity_pct:.2f}%")
    table.add_row("INSTRUMENTATION", f"{state.instrumentation_integrity_pct:.2f}%")
    table.add_row("AI ANOMALY", f"{state.network_anomaly_score*100:.1f}%")
    table.add_row("MC&A VARIANCE", f"{state.material_balance_delta:.4f}")
    table.add_row("ACCESS RISK", f"{state.access_risk_score*100:.1f}%")
    table.add_row("COMPLIANCE", f"{state.compliance_score_pct:.1f}%")
    table.add_row("AUDIT EVIDENCE", f"{state.audit_coverage_pct:.1f}%")
    table.add_row("KEY FINDING", report["findings"][0])
    return Panel(table, title="NUCLEARSHIELD // DEFENSIVE EVIDENCE REPORT", subtitle="synthetic evidence • advisory conclusions • human review", box=box.DOUBLE, border_style="cyan")


def save_report(state: FacilityState, output_dir: Path) -> tuple[Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    report = build_report(state)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    base = output_dir / f"nuclearshield_{state.scenario}_{stamp}"
    json_path = base.with_suffix(".json")
    txt_path = base.with_suffix(".txt")
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    lines = [
        "NUCLEARSHIELD DEFENSIVE EVIDENCE SUMMARY",
        "=" * 48,
        f"Generated: {report['generated_utc']}",
        f"Scenario: {report['scenario']}",
        f"Risk: {report['risk_level']}",
        f"Decision: {report['response_mode']}",
        f"Active alerts: {report['active_alerts']}",
        "",
        "FINDINGS",
        *[f"- {item}" for item in report["findings"]],
        "",
        "ASSURANCE",
        f"- Safety integrity: {state.safety_integrity_pct:.2f}%",
        f"- Instrumentation integrity: {state.instrumentation_integrity_pct:.2f}%",
        f"- Compliance readiness: {state.compliance_score_pct:.2f}%",
        f"- Audit evidence coverage: {state.audit_coverage_pct:.2f}%",
        "",
        "SAFEGUARDS",
        f"- MC&A variance: {state.material_balance_delta:.4f}",
        f"- Access risk: {state.access_risk_score*100:.2f}%",
        f"- Cyber-physical correlation: {state.cyber_physical_correlation*100:.2f}%",
        "",
        "SAFETY BOUNDARY",
        str(report["safety_boundary"]),
    ]
    txt_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, txt_path
