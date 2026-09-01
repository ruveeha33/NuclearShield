from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _status_panel() -> Panel:
    table = Table.grid(expand=True, padding=(0, 2))
    table.add_column(style="bold cyan", ratio=2)
    table.add_column(justify="right", ratio=1)
    table.add_row("Simulation Engine", "[bold green]READY[/bold green]")
    table.add_row("Safety Boundary", "[bold green]ENFORCED[/bold green]")
    table.add_row("Control Write Access", "[bold]DISABLED[/bold]")
    table.add_row("Evidence Source", "SYNTHETIC / LOCAL")
    table.add_row("AI Analysis", "[bold green]READY[/bold green]")
    return Panel(table, title="SYSTEM STATUS", box=box.ROUNDED)


def _menu_panel() -> Panel:
    table = Table.grid(expand=True, padding=(0, 1))
    table.add_column(style="bold cyan", width=6)
    table.add_column()
    table.add_row("[1]", "[bold]LAUNCH COMMAND WORKSTATION[/bold]\n[dim]Terminal command center + local Grafana/Prometheus monitoring[/dim]")
    table.add_row("[2]", "[bold]LAUNCH TERMINAL ANALYSIS[/bold]\n[dim]Terminal-only combined defensive simulation[/dim]")
    table.add_row("[3]", "[bold]RUN SYSTEM DIAGNOSTICS[/bold]\n[dim]Check local demonstration prerequisites[/dim]")
    table.add_row("[4]", "[bold]ARCHITECTURE & ASSURANCE[/bold]\n[dim]Review defense-in-depth architecture and software assurance gates[/dim]")
    table.add_row("[Q]", "QUIT")
    return Panel(table, title="OPERATIONS", subtitle="select a workstation function", box=box.ROUNDED)


def show_start_screen() -> None:
    console.clear()
    title = Table.grid(expand=True)
    title.add_column(justify="center")
    title.add_row("[bold cyan]N U C L E A R S H I E L D[/bold cyan]")
    title.add_row("[bold]Nuclear Cybersecurity & Safety Integrity Workstation[/bold]")
    title.add_row("[dim]Defensive educational simulation • synthetic evidence • read-only[/dim]")
    console.print(Panel(title, box=box.DOUBLE, padding=(1, 2)))
    console.print(_status_panel())
    console.print(_menu_panel())


def _run(*args: str) -> int:
    return subprocess.call([sys.executable, "-m", "nuclearshield", *args], cwd=_repo_root())


def main() -> None:
    while True:
        show_start_screen()
        choice = console.input("\n[bold cyan]Select operation > [/bold cyan]").strip().lower()
        if choice == "1":
            _run("--briefing", "--monitoring", "--scenario", "combined", "--report", "--export-report")
        elif choice == "2":
            _run("--briefing", "--scenario", "combined", "--report")
        elif choice == "3":
            _run("--self-check")
            console.input("\n[dim]Press Enter to return to NuclearShield...[/dim]")
        elif choice == "4":
            _run("--architecture")
            _run("--assurance")
            console.input("\n[dim]Press Enter to return to NuclearShield...[/dim]")
        elif choice in {"q", "quit", "exit", "0"}:
            console.print("[dim]NuclearShield workstation closed. No control actions were performed.[/dim]")
            return
        else:
            console.print("[yellow]Unknown selection. Choose 1, 2, 3, 4, or Q.[/yellow]")
            console.input("[dim]Press Enter to continue...[/dim]")


if __name__ == "__main__":
    main()
