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

from .dashboard import render_dashboard
from .metrics import start_metrics_server, update_metrics
from .model import FacilityState
from .simulator import FacilitySimulator

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
            time.sleep(2.5)
            webbrowser.open("http://localhost:3000")
            webbrowser.open("http://localhost:9090")
        threading.Thread(target=opener, daemon=True).start()
    return True


def run_dashboard(refresh: float = 1.0, seed: int | None = None) -> None:
    state = FacilityState()
    state.add_event("NuclearShield synthetic monitoring started")
    simulator = FacilitySimulator(seed=seed)
    start_metrics_server(9108)
    with Live(render_dashboard(state), refresh_per_second=4, screen=True) as live:
        while True:
            simulator.step(state)
            update_metrics(state)
            live.update(render_dashboard(state))
            time.sleep(refresh)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NuclearShield defensive educational simulation")
    parser.add_argument("--monitoring", action="store_true", help="start Grafana and Prometheus with Docker Compose")
    parser.add_argument("--no-browser", action="store_true", help="do not auto-open browser dashboards")
    parser.add_argument("--refresh", type=float, default=1.0, help="terminal refresh interval in seconds")
    parser.add_argument("--seed", type=int, default=None, help="deterministic simulation seed")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    console.print("[bold cyan]NuclearShield[/bold cyan] — safe educational simulation; no real nuclear/OT connectivity.")
    if args.monitoring:
        start_monitoring_stack(open_web=not args.no_browser)
    try:
        run_dashboard(refresh=max(0.25, args.refresh), seed=args.seed)
    except KeyboardInterrupt:
        console.print("\n[green]NuclearShield stopped safely.[/green]")
