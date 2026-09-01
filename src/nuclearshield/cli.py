from __future__ import annotations

import argparse
import shutil
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

from rich import box
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from .assurance import assurance_panel, threat_context_panel
from .dashboard import render_dashboard
from .metrics import start_metrics_server, update_metrics
from .model import FacilityState
from .reporting import report_panel, save_report
from .simulator import FacilitySimulator, SCENARIOS

console = Console()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def start_monitoring_stack(open_web: bool = True) -> bool:
    if shutil.which("docker") is None:
        console.print("[yellow]Docker not found.[/yellow] Terminal command center will still run.")
        return False
    compose = _repo_root() / "docker-compose.yml"
    try:
        subprocess.run(["docker", "compose", "-f", str(compose), "up", "-d"], check=True)
    except (subprocess.CalledProcessError, OSError):
        console.print("[yellow]Could not start Grafana/Prometheus. Terminal mode will continue.[/yellow]")
        return False
    if open_web:
        def opener() -> None:
            time.sleep(3.0)
            webbrowser.open("http://localhost:3000/d/nuclearshield-main")
            webbrowser.open("http://localhost:9090")
        threading.Thread(target=opener, daemon=True).start()
    return True


def show_architecture() -> None:
    console.print(Panel.fit(
        "ENTERPRISE / SOC\n      ↓ controlled monitoring path\nINDUSTRIAL DMZ\n      ↓ passive defensive evidence\n"
        "OT / SCADA MONITORING ─────→ AI / CORRELATION\n      ⇢ conceptual one-way evidence path\n"
        "SAFETY I&C (independent) ──→ INTEGRITY ASSURANCE\nPHYSICAL SECURITY ─────────→ ACCESS ANALYTICS\n"
        "MC&A SAFEGUARDS ───────────→ MATERIAL RECONCILIATION\n                ↓\nHUMAN REVIEW → AUDIT → COMPLIANCE EVIDENCE",
        title="NuclearShield Defense-in-Depth Architecture",
        subtitle="Synthetic defensive learning lab — not a deployment blueprint", box=box.DOUBLE,
    ))


def show_briefing(scenario: str) -> None:
    t = Table.grid(expand=True, padding=(0, 1)); t.add_column(style="bold cyan", width=21); t.add_column()
    t.add_row("MISSION", "Demonstrate layered nuclear-facility cyber defense using synthetic evidence only.")
    t.add_row("SCENARIO", scenario.upper())
    t.add_row("SAFETY", "No real reactor, PLC, SCADA, PACS, safety-I&C, or material system connectivity.")
    t.add_row("DETECTION", "Rule-based state checks + IsolationForest anomaly scoring + cross-domain correlation.")
    t.add_row("SAFEGUARDS", "MC&A variance and physical/access signals are simulated for educational review.")
    t.add_row("OBSERVABILITY", "Terminal command center + Prometheus metrics + Grafana visualization.")
    t.add_row("DECISION", "System is advisory; high-risk states escalate to HUMAN REVIEW.")
    console.print(Panel(t, title="NUCLEARSHIELD // PRE-MISSION BRIEFING", border_style="cyan", box=box.DOUBLE))


def system_check() -> int:
    checks = [
        ("Python runtime", True, "available"),
        ("Docker CLI", shutil.which("docker") is not None, "required only for Grafana/Prometheus"),
        ("Compose file", (_repo_root() / "docker-compose.yml").exists(), "monitoring stack definition"),
        ("Grafana provisioning", (_repo_root() / "monitoring" / "grafana").exists(), "local dashboard configuration"),
        ("Prometheus config", (_repo_root() / "monitoring" / "prometheus.yml").exists(), "metrics scraper configuration"),
    ]
    table = Table(title="NUCLEARSHIELD READINESS CHECK", box=box.SIMPLE_HEAVY)
    table.add_column("Component"); table.add_column("State", justify="center"); table.add_column("Purpose")
    for name, ok, detail in checks:
        table.add_row(name, "[bold green]READY[/bold green]" if ok else "[yellow]OPTIONAL / MISSING[/yellow]", detail)
    console.print(table)
    console.print("[dim]Docker is optional for terminal-only exam mode; all facility signals remain synthetic.[/dim]")
    return 0 if all(ok for name, ok, _ in checks if name != "Docker CLI") else 1


def run_dashboard(scenario: str = "normal", refresh_rate: float = 4.0, samples: int = 0, seed: int | None = None, fullscreen: bool = True) -> FacilityState:
    state = FacilityState(scenario=scenario); state.add_event("NuclearShield synthetic monitoring session started", "SYSTEM")
    simulator = FacilitySimulator(scenario=scenario, seed=seed); start_metrics_server(9108)
    refresh_rate = max(1.0, min(refresh_rate, 10.0)); delay = 1.0 / refresh_rate
    try:
        with Live(render_dashboard(state), refresh_per_second=refresh_rate, screen=fullscreen, transient=False, vertical_overflow="crop") as live:
            i = 0
            while samples <= 0 or i < samples:
                simulator.step(state); update_metrics(state); live.update(render_dashboard(state), refresh=True); time.sleep(delay); i += 1
    except KeyboardInterrupt:
        state.add_event("Operator ended synthetic monitoring session", "SYSTEM")
    return state


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NuclearShield defensive educational nuclear-cyber simulation")
    parser.add_argument("--monitoring", action="store_true", help="start Grafana and Prometheus with Docker Compose")
    parser.add_argument("--no-browser", action="store_true", help="do not auto-open browser dashboards")
    parser.add_argument("--scenario", choices=sorted(SCENARIOS), default="combined", help="synthetic exam scenario")
    parser.add_argument("--refresh-rate", type=float, default=4.0, help="terminal frames per second (1-10)")
    parser.add_argument("--samples", type=int, default=0, help="number of frames; 0 means run until Ctrl+C")
    parser.add_argument("--seed", type=int, default=132, help="deterministic simulation seed")
    parser.add_argument("--windowed", action="store_true", help="do not use alternate-screen fullscreen mode")
    parser.add_argument("--architecture", action="store_true", help="print the conceptual architecture and exit")
    parser.add_argument("--briefing", action="store_true", help="show the pre-mission exam briefing before launch")
    parser.add_argument("--self-check", action="store_true", help="check local exam-demo prerequisites and exit")
    parser.add_argument("--assurance", action="store_true", help="show nuclear software DevSecOps assurance gates and exit")
    parser.add_argument("--threat-context", action="store_true", help="show safe nuclear-sector defensive threat context and exit")
    parser.add_argument("--report", action="store_true", help="show an end-of-session defensive evidence report")
    parser.add_argument("--export-report", action="store_true", help="save JSON and text evidence reports under reports/")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.architecture: show_architecture(); return
    if args.assurance: console.print(assurance_panel()); return
    if args.threat_context: console.print(threat_context_panel()); return
    if args.self_check: raise SystemExit(system_check())
    if args.briefing:
        show_briefing(args.scenario); console.print("[dim]Starting command center in 2 seconds...[/dim]"); time.sleep(2.0)
    summary = Table.grid(padding=(0, 1)); summary.add_row("[bold cyan]NuclearShield[/bold cyan]", "Facility Protection Command")
    summary.add_row("Mode", "safe synthetic / defensive / read-only"); summary.add_row("Scenario", args.scenario)
    console.print(Panel(summary, title="COMMAND SESSION INITIALIZING", box=box.DOUBLE))
    if args.monitoring: start_monitoring_stack(open_web=not args.no_browser)
    state = run_dashboard(args.scenario, args.refresh_rate, max(0, args.samples), args.seed, not args.windowed)
    console.print("\n[green]NuclearShield session closed safely.[/green]")
    if args.report or args.export_report: console.print(report_panel(state))
    if args.export_report:
        json_path, txt_path = save_report(state, _repo_root() / "reports")
        console.print(f"[cyan]Evidence exported:[/cyan] {json_path.name}  |  {txt_path.name}")
