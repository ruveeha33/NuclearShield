from __future__ import annotations

from rich import box
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .model import FacilityState


def _meter(value: float, width: int = 18) -> str:
    value = max(0.0, min(100.0, float(value)))
    filled = round(width * value / 100)
    return "█" * filled + "░" * (width - filled)


def _risk_style(level: str) -> str:
    return {
        "CRITICAL": "bold red",
        "HIGH": "bold yellow",
        "ELEVATED": "yellow",
        "NORMAL": "bold green",
    }.get(level, "white")


def _health(ok: bool) -> str:
    return "[bold green]HEALTHY[/bold green]" if ok else "[bold red]REVIEW[/bold red]"


def _header(s: FacilityState) -> Panel:
    grid = Table.grid(expand=True)
    grid.add_column(ratio=3)
    grid.add_column(justify="center", ratio=2)
    grid.add_column(justify="right", ratio=2)
    style = _risk_style(s.risk_level)
    grid.add_row(
        "[bold cyan]NUCLEARSHIELD[/bold cyan]  [dim]Nuclear Cyber Defense Operations Console[/dim]",
        f"Scenario: [bold]{s.scenario.upper()}[/bold]",
        f"Frame {s.tick:04d}  |  [{style}]{s.risk_level}[/{style}]",
    )
    return Panel(grid, box=box.HEAVY, padding=(0, 1))


def _facility_map(s: FacilityState) -> Panel:
    t = Table.grid(expand=True)
    for _ in range(6):
        t.add_column(justify="center")
    t.add_row(
        "[cyan]ENTERPRISE / SOC[/cyan]",
        "[cyan]INDUSTRIAL DMZ[/cyan]",
        "[cyan]OT / SCADA[/cyan]",
        "[cyan]SAFETY I&C[/cyan]",
        "[cyan]PHYSICAL SECURITY[/cyan]",
        "[cyan]MC&A SAFEGUARDS[/cyan]",
    )
    t.add_row("→", "→", "→", "⇢ one-way evidence", "↔ correlation", "↔ audit")
    t.add_row(
        _health(s.enterprise_zone_ok),
        _health(s.dmz_zone_ok),
        _health(s.scada_zone_ok),
        _health(s.safety_zone_ok),
        _health(s.physical_security_ok),
        _health(s.material_accounting_ok),
    )
    return Panel(
        t,
        title="[bold]DEFENSE-IN-DEPTH DIGITAL FACILITY MAP[/bold]",
        subtitle="Conceptual segmentation • passive monitoring • synthetic data only",
        box=box.ROUNDED,
    )


def _safety_panel(s: FacilityState) -> Panel:
    t = Table.grid(padding=(0, 1), expand=True)
    t.add_column()
    t.add_column(justify="right")
    t.add_row("Reactor power", f"{s.reactor_power_pct:6.2f} %")
    t.add_row("Coolant temperature", f"{s.coolant_temp_c:6.2f} °C")
    t.add_row("Primary pressure", f"{s.primary_pressure_mpa:6.3f} MPa")
    t.add_row("Neutron flux", f"{s.neutron_flux_pct:6.2f} %")
    t.add_row("Safety integrity", f"{s.safety_integrity_pct:6.2f} %")
    t.add_row("Instrumentation integrity", f"{s.instrumentation_integrity_pct:6.2f} %")
    return Panel(t, title="SAFETY SYSTEM INTEGRITY", subtitle="Illustrative telemetry", box=box.ROUNDED)


def _ot_panel(s: FacilityState) -> Panel:
    t = Table.grid(padding=(0, 1), expand=True)
    t.add_column()
    t.add_column(justify="right")
    t.add_row("SCADA zone", _health(s.scada_zone_ok))
    t.add_row("One-way gateway", _health(s.data_diode_ok))
    t.add_row("AI network anomaly", f"{s.network_anomaly_score * 100:5.1f}%")
    t.add_row("Configuration drift", f"{s.configuration_drift_score * 100:5.1f}%")
    t.add_row("Firmware integrity", f"{s.firmware_integrity_pct:5.2f}%")
    t.add_row("Control writes", "[bold green]DISABLED[/bold green]")
    return Panel(t, title="OT / SCADA PROTECTION", subtitle="Passive defensive monitoring", box=box.ROUNDED)


def _risk_panel(s: FacilityState) -> Panel:
    fused = max(
        s.network_anomaly_score,
        s.access_risk_score,
        s.configuration_drift_score,
        s.cyber_physical_correlation,
        min(1.0, s.material_balance_delta / 0.16),
    )
    style = _risk_style(s.risk_level)
    body = Text()
    body.append(f"{_meter(fused * 100)}  {fused * 100:5.1f}%\n", style=style)
    body.append(f"Overall: {s.risk_level}\n", style=style)
    body.append(f"AI anomaly       {s.network_anomaly_score * 100:5.1f}%\n")
    body.append(f"Access risk      {s.access_risk_score * 100:5.1f}%\n")
    body.append(f"Cyber-physical   {s.cyber_physical_correlation * 100:5.1f}%\n")
    body.append(f"Decision: {s.response_mode}", style="bold cyan")
    return Panel(body, title="AI RISK FUSION & DECISION", box=box.ROUNDED)


def _material_panel(s: FacilityState) -> Panel:
    t = Table.grid(padding=(0, 1), expand=True)
    t.add_column()
    t.add_column(justify="right")
    t.add_row("MC&A status", _health(s.material_accounting_ok))
    t.add_row("Balance variance", f"{s.material_balance_delta:.4f}")
    t.add_row("Access / insider risk", f"{s.access_risk_score * 100:5.1f}%")
    t.add_row("Physical security", _health(s.physical_security_ok))
    t.add_row("Correlation", f"{s.cyber_physical_correlation * 100:5.1f}%")
    t.add_row("Safeguards action", "HUMAN REVIEW" if not s.material_accounting_ok else "MONITOR")
    return Panel(t, title="NUCLEAR MATERIAL & PHYSICAL-CYBER", box=box.ROUNDED)


def _evidence_panel(s: FacilityState) -> Panel:
    t = Table(title="LIVE ASSURANCE EVIDENCE", expand=True, box=box.SIMPLE)
    t.add_column("Evidence")
    t.add_column("State", justify="right")
    t.add_row("IEC 62645 mapping", "TRACKED")
    t.add_row("NRC RG 5.71 mapping", "TRACKED")
    t.add_row("IAEA guidance mapping", "TRACKED")
    t.add_row("Compliance readiness", f"{s.compliance_score_pct:5.1f}%")
    t.add_row("Audit coverage", f"{s.audit_coverage_pct:5.1f}%")
    t.add_row("Active alerts", str(s.active_alerts))
    t.add_row("Synthetic telemetry", "ENABLED")
    t.add_row("Real OT connectivity", "DISABLED")
    return Panel(t, box=box.ROUNDED)


def _event_panel(s: FacilityState) -> Panel:
    lines = s.event_log or ["[green]SYSTEM[/green] Baseline synthetic evidence within classroom bands"]
    return Panel("\n".join(lines), title="ACTIVE SECURITY / SAFEGUARDS EVENT FEED", box=box.ROUNDED)


def _footer() -> Panel:
    return Panel(
        "[bold]BOUNDARY:[/bold] SYNTHETIC • DEFENSIVE • READ-ONLY EDUCATIONAL SIMULATION   "
        "[dim]No real reactor, PLC, SCADA, safety, PACS or nuclear-material system connectivity. "
        "Grafana :3000 • Prometheus :9090 • Metrics :9108 • Ctrl+C exit[/dim]",
        box=box.HEAVY,
        padding=(0, 1),
    )


def render_dashboard(s: FacilityState) -> Layout:
    """Build a dense SOC-style live terminal layout inspired by AquaSentinel's UX only."""
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="facility", size=7),
        Layout(name="body", ratio=1, minimum_size=14),
        Layout(name="events", size=7),
        Layout(name="footer", size=3),
    )
    layout["body"].split_row(Layout(name="left"), Layout(name="middle"), Layout(name="right"))
    layout["left"].split_column(Layout(name="safety"), Layout(name="ot"))
    layout["middle"].split_column(Layout(name="risk"), Layout(name="material"))

    layout["header"].update(_header(s))
    layout["facility"].update(_facility_map(s))
    layout["safety"].update(_safety_panel(s))
    layout["ot"].update(_ot_panel(s))
    layout["risk"].update(_risk_panel(s))
    layout["material"].update(_material_panel(s))
    layout["right"].update(_evidence_panel(s))
    layout["events"].update(_event_panel(s))
    layout["footer"].update(_footer())
    return layout
