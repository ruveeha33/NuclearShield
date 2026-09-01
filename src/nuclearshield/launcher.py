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
    table.add_row("Evidence Package", "[yellow]NO DATA LOADED[/yellow]")
    table.add_row("Analysis Engine", "[yellow]WAITING FOR INPUT[/yellow]")
    table.add_row("Control Write Access", "[bold]DISABLED[/bold]")
    table.add_row("Data Policy", "LOCAL FILES ONLY")
    table.add_row("Finding Policy", "NO DATA → NO FINDINGS")
    return Panel(table, title="SYSTEM STATUS", box=box.ROUNDED)


def _menu_panel() -> Panel:
    table = Table.grid(expand=True, padding=(0, 1))
    table.add_column(style="bold cyan", width=6)
    table.add_column()
    table.add_row("[1]", "[bold]LOAD EVIDENCE PACKAGE[/bold]\n[dim]Analyze one or more CSV, JSON, JSONL, or XLSX files[/dim]")
    table.add_row("[2]", "[bold]RUN SYSTEM DIAGNOSTICS[/bold]\n[dim]Check local analysis prerequisites[/dim]")
    table.add_row("[3]", "[bold]ARCHITECTURE & ASSURANCE[/bold]\n[dim]Review the read-only evidence-analysis design[/dim]")
    table.add_row("[Q]", "QUIT")
    return Panel(table, title="OPERATIONS", subtitle="select a workstation function", box=box.ROUNDED)


def show_start_screen() -> None:
    console.clear()
    title = Table.grid(expand=True)
    title.add_column(justify="center")
    title.add_row("[bold cyan]N U C L E A R S H I E L D[/bold cyan]")
    title.add_row("[bold]Nuclear Cybersecurity & Safety Integrity Workstation[/bold]")
    title.add_row("[dim]Schema-driven • local evidence • read-only analysis[/dim]")
    console.print(Panel(title, box=box.DOUBLE, padding=(1, 2)))
    console.print(_status_panel())
    console.print(_menu_panel())


def _run(*args: str) -> int:
    return subprocess.call([sys.executable, "-m", "nuclearshield", *args], cwd=_repo_root())


def _collect_paths() -> list[str]:
    console.print("\n[bold]Evidence selection[/bold]")
    console.print("[dim]Enter file paths separated by semicolons. You can paste paths from File Explorer.[/dim]")
    raw = console.input("[bold cyan]Files > [/bold cyan]").strip()
    if not raw:
        return []
    paths = []
    for item in raw.split(";"):
        cleaned = item.strip().strip('"').strip("'")
        if cleaned:
            paths.append(cleaned)
    return paths


def main() -> None:
    while True:
        show_start_screen()
        choice = console.input("\n[bold cyan]Select operation > [/bold cyan]").strip().lower()
        if choice == "1":
            paths = _collect_paths()
            if not paths:
                console.print("[yellow]No files selected. Nothing was analyzed.[/yellow]")
            else:
                export = console.input("[cyan]Export JSON/TXT report after analysis? [Y/n] > [/cyan]").strip().lower()
                args = ["--files", *paths]
                if export not in {"n", "no"}:
                    args.append("--export-report")
                _run(*args)
            console.input("\n[dim]Press Enter to return to NuclearShield...[/dim]")
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
