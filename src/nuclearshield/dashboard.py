from __future__ import annotations

from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .model import FacilityState


def _risk_style(level: str) -> str:
    return {"CRITICAL": "bold red", "HIGH": "bold yellow", "ELEVATED": "yellow", "NORMAL": "bold green"}.get(level, "white")


def _lamp(ok: bool, healthy: str = "SECURE", review: str = "REVIEW") -> str:
    return f"[bold green]● {healthy}[/bold green]" if ok else f"[bold red]● {review}[/bold red]"


def _bar(value: float, width: int = 20) -> str:
    value = max(0.0, min(100.0, value))
    filled = round(width * value / 100)
    return "▰" * filled + "▱" * (width - filled)


def _masthead(s: FacilityState) -> Panel:
    risk = _risk_style(s.risk_level)
    title = Text("NUCLEARSHIELD", style="bold white")
    title.append("  /  FACILITY PROTECTION COMMAND", style="bold cyan")
    meta = Table.grid(expand=True)
    meta.add_column(ratio=4)
    meta.add_column(justify="center", ratio=2)
    meta.add_column(justify="right", ratio=2)
    meta.add_row(title, f"SIMULATION  {s.scenario.upper()}", f"[{risk}]DEFCON-CYBER {s.risk_level}[/{risk}]  T+{s.tick:04d}")
    return Panel(meta, box=box.DOUBLE, border_style="cyan", padding=(0, 1))


def _containment_core(s: FacilityState) -> Panel:
    left = Table.grid(padding=(0, 1))
    left.add_column(); left.add_column(justify="right")
    left.add_row("THERMAL POWER", f"{s.reactor_power_pct:6.2f}%")
    left.add_row("PRIMARY TEMP", f"{s.coolant_temp_c:6.2f} °C")
    left.add_row("PRIMARY PRESS", f"{s.primary_pressure_mpa:6.3f} MPa")
    left.add_row("NEUTRON FLUX", f"{s.neutron_flux_pct:6.2f}%")

    right = Table.grid(padding=(0, 1))
    right.add_column(); right.add_column(justify="right")
    right.add_row("SAFETY I&C", f"{s.safety_integrity_pct:6.2f}%")
    right.add_row("INSTRUMENTS", f"{s.instrumentation_integrity_pct:6.2f}%")
    right.add_row("FIRMWARE", f"{s.firmware_integrity_pct:6.2f}%")
    right.add_row("WRITE PATH", "[bold green]LOCKED[/bold green]")

    core = Text(justify="center")
    core.append("╭──────────────╮\n", style="cyan")
    core.append("│  CONTAINMENT │\n", style="bold white")
    core.append("│  DIGITAL TWIN│\n", style="bold cyan")
    core.append("╰──────┬───────╯\n", style="cyan")
    core.append("       │ passive evidence\n", style="dim")
    core.append("       ▼", style="cyan")

    return Panel(Columns([left, Align.center(core), right], expand=True, equal=True), title="FACILITY CORE / SAFETY ENVELOPE", border_style="bright_blue", box=box.HEAVY)


def _perimeter(s: FacilityState) -> Panel:
    grid = Table.grid(expand=True)
    for _ in range(6): grid.add_column(justify="center")
    grid.add_row("ENTERPRISE", "DMZ", "OT-SCADA", "SAFETY", "PACS", "MC&A")
    grid.add_row(
        _lamp(s.enterprise_zone_ok), _lamp(s.dmz_zone_ok), _lamp(s.scada_zone_ok),
        _lamp(s.safety_zone_ok), _lamp(s.physical_security_ok), _lamp(s.material_accounting_ok),
    )
    grid.add_row("SOC", "broker", "observe", "independent", "access", "safeguards")
    return Panel(grid, title="PROTECTION RINGS", subtitle="segmented trust zones • one-way evidence paths • no control capability", box=box.SQUARE)


def _mission_risk(s: FacilityState) -> Panel:
    fused = max(s.network_anomaly_score, s.access_risk_score, s.configuration_drift_score, s.cyber_physical_correlation, min(1.0, s.material_balance_delta / 0.16)) * 100
    style = _risk_style(s.risk_level)
    body = Text()
    body.append(f"{_bar(fused)} {fused:5.1f}%\n", style=style)
    body.append(f"MISSION RISK  {s.risk_level}\n\n", style=style)
    body.append(f"Network anomaly   {s.network_anomaly_score*100:5.1f}%\n")
    body.append(f"Config drift      {s.configuration_drift_score*100:5.1f}%\n")
    body.append(f"Access/insider    {s.access_risk_score*100:5.1f}%\n")
    body.append(f"Cyber-physical    {s.cyber_physical_correlation*100:5.1f}%\n")
    body.append(f"\nORDER: {s.response_mode}", style="bold cyan")
    return Panel(body, title="COMMAND ASSESSMENT", border_style="yellow", box=box.HEAVY)


def _safeguards(s: FacilityState) -> Panel:
    t = Table.grid(expand=True, padding=(0, 1)); t.add_column(); t.add_column(justify="right")
    t.add_row("Material account", _lamp(s.material_accounting_ok, "BALANCED", "RECONCILE"))
    t.add_row("Balance variance", f"{s.material_balance_delta:.4f}")
    t.add_row("Physical security", _lamp(s.physical_security_ok))
    t.add_row("Access analytics", f"{s.access_risk_score*100:5.1f}%")
    t.add_row("Cross-domain corr.", f"{s.cyber_physical_correlation*100:5.1f}%")
    t.add_row("Disposition", "HUMAN REVIEW" if not s.material_accounting_ok else "CONTINUOUS MONITOR")
    return Panel(t, title="SAFEGUARDS WATCH", border_style="magenta", box=box.SQUARE)


def _assurance(s: FacilityState) -> Panel:
    t = Table.grid(expand=True, padding=(0, 1)); t.add_column(); t.add_column(justify="right")
    t.add_row("IEC 62645", "EVIDENCE MAPPED")
    t.add_row("NRC RG 5.71", "EVIDENCE MAPPED")
    t.add_row("IAEA guidance", "EVIDENCE MAPPED")
    t.add_row("Readiness", f"{s.compliance_score_pct:5.1f}%")
    t.add_row("Audit coverage", f"{s.audit_coverage_pct:5.1f}%")
    t.add_row("Alerts", str(s.active_alerts))
    return Panel(t, title="ASSURANCE BOARD", border_style="green", box=box.SQUARE)


def _event_ticker(s: FacilityState) -> Panel:
    entries = s.event_log[-4:] if s.event_log else ["SYSTEM // baseline synthetic facility evidence nominal"]
    numbered = "\n".join(f"{i+1:02d}  {line}" for i, line in enumerate(entries))
    return Panel(numbered, title="SECURITY OPERATIONS TICKER", border_style="cyan", box=box.MINIMAL_DOUBLE_HEAD)


def _footer() -> Panel:
    return Panel("[bold cyan]SIMULATION BOUNDARY[/bold cyan]  READ-ONLY • SYNTHETIC • DEFENSIVE   |   Real OT/PACS/SCADA: DISCONNECTED   |   Grafana :3000   Prometheus :9090   Metrics :9108   Ctrl+C EXIT", box=box.DOUBLE, padding=(0, 1))


def render_dashboard(s: FacilityState) -> Layout:
    """NuclearShield's distinct facility-protection command-center terminal."""
    layout = Layout()
    layout.split_column(
        Layout(name="masthead", size=3), Layout(name="core", size=9), Layout(name="rings", size=6),
        Layout(name="command", ratio=1, minimum_size=11), Layout(name="ticker", size=7), Layout(name="footer", size=3),
    )
    layout["command"].split_row(Layout(name="risk", ratio=5), Layout(name="safeguards", ratio=5), Layout(name="assurance", ratio=4))
    layout["masthead"].update(_masthead(s))
    layout["core"].update(_containment_core(s))
    layout["rings"].update(_perimeter(s))
    layout["risk"].update(_mission_risk(s))
    layout["safeguards"].update(_safeguards(s))
    layout["assurance"].update(_assurance(s))
    layout["ticker"].update(_event_ticker(s))
    layout["footer"].update(_footer())
    return layout
