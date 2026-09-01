from __future__ import annotations

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
    table.add_row("Evidence Package", "[bold yellow]NO DATA LOADED[/bold yellow]")
    table.add_row("Analysis Engine", "[bold yellow]WAITING FOR INPUT[/bold yellow]")
    table.add_row("Safety Boundary", "[bold green]ENFORCED[/bold green]")
    table.add_row("Control Write Access", "[bold]DISABLED[/bold]")
    table.add_row("Data Policy", "LOCAL FILES ONLY")
    return Panel(table, title="SYSTEM STATUS", box=box.ROUNDED)


def _menu_panel() -> Panel:
    table = Table.grid(expand=True, padding=(0, 1))
    table.add_column(style="bold cyan", width=6)
    table.add_column()
    table.add_row("[1]", "[bold]LOAD EVIDENCE PACKAGE[/bold]\n[dim]Analyze only the files supplied by the operator[/dim]")
    table.add_row("[2]", "[bold]SYSTEM DIAGNOSTICS[/bold]\n[dim]Verify the local analysis environment[/dim]")
    table.add_row("[3]", "[bold]ARCHITECTURE & ASSURANCE[/bold]\n[dim]Review the defensive analysis architecture[/dim]")
    table.add_row("[Q]", "QUIT")
    return Panel(table, title="OPERATIONS", subtitle="no analysis begins until evidence is supplied", box=box.ROUNDED)


def show_start_screen() -> None:
    console.clear()
    title = Table.grid(expand=True)
    title.add_column(justify="center")
    title.add_row("[bold cyan]N U C L E A R S H I E L D[/bold cyan]")
    title.add_row("[bold]Nuclear Cybersecurity & Safety Integrity Workstation[/bold]")
    title.add_row("[dim]Defensive • read-only • operator-supplied evidence[/dim]")
    console.print(Panel(title, box=box.DOUBLE, padding=(1, 2)))
    console.print(_status_panel())
    console.print(_menu_panel())


def _run(*args: str) -> int:
    return subprocess.call([sys.executable, "-m", "nuclearshield", *args], cwd=_repo_root())


def _evidence_placeholder() -> None:
    console.print(Panel(
        "NuclearShield is waiting for operator-supplied evidence files.\n\n"
        "Once files are provided, this workflow will identify each file, validate its structure, "
        "classify its evidence domain, analyze its records, and populate the terminal/reporting/monitoring views.\n\n"
        "[bold yellow]No synthetic incident or automatic scenario has been started.[/bold yellow]",
        title="EVIDENCE INTAKE",
        box=box.DOUBLE,
    ))
    console.input("\n[dim]Press Enter to return to NuclearShield...[/dim]")


def main() -> None:
    while True:
        show_start_screen()
        choice = console.input("\n[bold cyan]Select operation > [/bold cyan]").strip().lower()
        if choice == "1":
            _evidence_placeholder()
        elif choice == "2":
            _run("--self-check")
            console.input("\n[dim]Press Enter to return to NuclearShield...[/dim]")
        elif choice == "3":
            _run("--architecture")
            _run("--assurance")
            console.input("\n[dim]Press Enter to return to NuclearShield...[/dim]")
        elif choice in {"q", "quit", "exit", "0"}:
            console.print("[dim]NuclearShield workstation closed. No control actions were performed.[/dim]")
            return
        else:
            console.print("[yellow]Unknown selection. Choose 1, 2, 3, or Q.[/yellow]")
            console.input("[dim]Press Enter to continue...[/dim]")


if __name__ == "__main__":
    main()
