from __future__ import annotations

from rich.align import Align
from rich.console import Group
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from .model import FacilityState


def _status(ok: bool) -> Text:
    return Text("HEALTHY" if ok else "ATTENTION", style="bold green" if ok else "bold red")


def _score(value: float) -> Text:
    style = "bold green" if value < 0.30 else "bold yellow" if value < 0.55 else "bold red"
    return Text(f"{value:.2f}", style=style)


def render_dashboard(s: FacilityState) -> Layout:
    layout = Layout()
    layout.split_column(Layout(name="header", size=4), Layout(name="body"), Layout(name="footer", size=3))
    layout["body"].split_row(Layout(name="left", ratio=1), Layout(name="right", ratio=1))
    layout["left"].split_column(Layout(name="plant"), Layout(name="zones"))
    layout["right"].split_column(Layout(name="threat"), Layout(name="events"))

    title = Text("NUCLEARSHIELD  //  DEFENSIVE EDUCATIONAL DIGITAL FACILITY", style="bold cyan")
    subtitle = Text("Synthetic telemetry • no real SCADA/PLC connection • safety-preserving simulation", style="dim")
    layout["header"].update(Panel(Align.center(Group(title, subtitle)), border_style="cyan"))

    plant = Table.grid(expand=True)
    plant.add_column(); plant.add_column(justify="right")
    plant.add_row("Reactor power", f"{s.reactor_power_pct:6.2f} %")
    plant.add_row("Coolant temperature", f"{s.coolant_temp_c:6.2f} °C")
    plant.add_row("Primary pressure", f"{s.primary_pressure_mpa:6.3f} MPa")
    plant.add_row("Neutron flux", f"{s.neutron_flux_pct:6.2f} %")
    plant.add_row("Safety integrity", f"{s.safety_integrity_pct:6.2f} %")
    layout["plant"].update(Panel(plant, title="SIMULATED PLANT TELEMETRY", border_style="blue"))

    zones = Table.grid(expand=True)
    zones.add_column(); zones.add_column(justify="right")
    zones.add_row("SCADA security zone", _status(s.scada_zone_ok))
    zones.add_row("Safety-system zone", _status(s.safety_zone_ok))
    zones.add_row("Data diode / one-way path", _status(s.data_diode_ok))
    zones.add_row("Physical-security zone", _status(s.physical_security_ok))
    zones.add_row("IEC/NRC/IAEA readiness", f"{s.compliance_score_pct:.1f} %")
    layout["zones"].update(Panel(zones, title="DEFENSE-IN-DEPTH & COMPLIANCE", border_style="magenta"))

    threat = Table.grid(expand=True)
    threat.add_column(); threat.add_column(justify="right")
    threat.add_row("AI anomaly score", _score(s.network_anomaly_score))
    threat.add_row("Access / insider risk", _score(s.access_risk_score))
    threat.add_row("MC&A balance variance", f"{s.material_balance_delta:.3f}")
    alert_style = "bold green" if s.active_alerts == 0 else "bold red"
    threat.add_row("Active alerts", Text(str(s.active_alerts), style=alert_style))
    threat.add_row("Response mode", Text("SAFETY-PRESERVING CONTAINMENT", style="bold cyan"))
    layout["threat"].update(Panel(threat, title="AI THREAT & MATERIAL SECURITY", border_style="yellow"))

    event_text = "\n".join(s.event_log) if s.event_log else "Waiting for synthetic events…"
    layout["events"].update(Panel(event_text, title="SECURITY EVENT STREAM", border_style="green"))

    layout["footer"].update(Panel("[bold]Controls:[/bold] Ctrl+C exit  •  Grafana http://localhost:3000  •  Prometheus http://localhost:9090  •  Metrics :9108", border_style="cyan"))
    return layout
