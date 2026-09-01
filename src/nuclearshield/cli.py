from __future__ import annotations

import argparse
import shutil
import subprocess
import threading
import time
import webbrowser
from pathlib import Path

from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.table import Table

from .dashboard import render_dashboard
from .metrics import start_metrics_server, update_metrics
from .model import FacilityState
from .simulator import FacilitySimulator, SCENARIOS

console = Console()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def start_monitoring_stack(open_web: bool = True) -> bool:
    if shutil.which("docker") is None:
        console.print("[yellow]Docker not found.[/yellow] Terminal dashboard will still run.")
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
        "ENTERPRISE / SOC\n"
        "      ↓ controlled monitoring path\n"
        "INDUSTRIAL DMZ\n"
        "      ↓ passive defensive evidence\n"
        "OT / SCADA MONITORING ─────→ AI / CORRELATION\n"
        "      ⇢ conceptual one-way evidence path\n"
        "SAFETY I&C (independent) ──→ INTEGRITY ASSURANCE\n"
        "PHYSICAL SECURITY ─────────→ ACCESS ANALYTICS\n"
        "MC&A SAFEGUARDS ───────────→ MATERIAL RECONCILIATION\n"
        "                ↓\n"
        "HUMAN REVIEW → AUDIT → COMPLIANCE EVIDENCE",
        title="NuclearShield Defense-in-Depth Architecture",
        subtitle="Synthetic defensive learning lab — not a deployment blueprint",
    ))


def run_dashboard(
    scenario: str = "normal",
    refresh_rate: float = 4.0,
    samples: int = 0,
    seed: int | None = None,
    fullscreen: bool = True,
) -> None:
    state = FacilityState(scenario=scenario)
    state.add_event("NuclearShield synthetic monitoring session started", "SYSTEM")
    simulator = FacilitySimulator(scenario=scenario, seed=seed)
    start_metrics_server(9108)
    refresh_rate = max(1.0, min(refresh_rate, 10.0))
    delay = 1.0 / refresh_rate

    with Live(
        render_dashboard(state),
        refresh_per_second=refresh_rate,
        screen=fullscreen,
        transient=False,
        vertical_overflow="crop",
    ) as live:
        i = 0
        while samples <= 0 or i < samples:
            simulator.step(state)
            update_metrics(state)
            live.update(render_dashboard(state), refresh=True)
            time.sleep(delay)
            i += 1


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
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.architecture:
        show_architecture()
        return

    summary = Table.grid(padding=(0, 1))
    summary.add_row("[bold cyan]NuclearShield[/bold cyan]", "Advanced Nuclear Facility Cybersecurity Platform")
    summary.add_row("Mode", "safe synthetic / defensive / read-only")
    summary.add_row("Scenario", args.scenario)
    console.print(Panel(summary, title="STARTING DEFENSIVE LAB", box=None))

    if args.monitoring:
        start_monitoring_stack(open_web=not args.no_browser)
    try:
        run_dashboard(
            scenario=args.scenario,
            refresh_rate=args.refresh_rate,
            samples=max(0, args.samples),
            seed=args.seed,
            fullscreen=not args.windowed,
        )
    except KeyboardInterrupt:
        console.print("\n[green]NuclearShield stopped safely.[/green]")
