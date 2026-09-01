from __future__ import annotations

import subprocess
import sys
import webbrowser
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()
GRAFANA_URL = "http://localhost:3000/d/nuclearshield-main"
PROMETHEUS_URL = "http://localhost:9090"
METRICS_URL = "http://localhost:9108/metrics"
SUPPORTED = {".csv", ".json", ".jsonl", ".xlsx"}


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _status_panel() -> Panel:
    table = Table.grid(expand=True, padding=(0, 2)); table.add_column(style="bold cyan", ratio=2); table.add_column(justify="right", ratio=1)
    table.add_row("Evidence Package", "[yellow]NO DATA LOADED[/yellow]")
    table.add_row("Analysis Engine", "[yellow]WAITING FOR INPUT[/yellow]")
    table.add_row("Control Write Access", "[bold]DISABLED[/bold]")
    table.add_row("Data Policy", "LOCAL FILES ONLY"); table.add_row("Finding Policy", "NO DATA → NO FINDINGS")
    return Panel(table, title="SYSTEM STATUS", box=box.ROUNDED)


def _menu_panel() -> Panel:
    table=Table.grid(expand=True,padding=(0,1)); table.add_column(style="bold cyan",width=6); table.add_column()
    table.add_row("[1]","[bold]LOAD + ANALYZE EVIDENCE[/bold]\n[dim]Analyze CSV, JSON, JSONL, or XLSX files[/dim]")
    table.add_row("[2]","[bold]ANALYZE + OPEN MONITORING[/bold]\n[dim]Analyze files, start Prometheus/Grafana, and open Grafana[/dim]")
    table.add_row("[3]","[bold]OPEN GRAFANA[/bold]\n[dim]Open the local evidence dashboard in your browser[/dim]")
    table.add_row("[4]","[bold]OPEN PROMETHEUS[/bold]\n[dim]Open the local Prometheus query interface[/dim]")
    table.add_row("[5]","[bold]OPEN RAW METRICS[/bold]\n[dim]View the evidence metrics exported by this workstation[/dim]")
    table.add_row("[6]","[bold]SYSTEM DIAGNOSTICS[/bold]\n[dim]Check local analysis and monitoring prerequisites[/dim]")
    table.add_row("[7]","[bold]ARCHITECTURE & ASSURANCE[/bold]\n[dim]Review the read-only evidence-analysis design[/dim]")
    table.add_row("[Q]","QUIT")
    return Panel(table,title="OPERATIONS",subtitle="select a workstation function",box=box.ROUNDED)


def show_start_screen() -> None:
    console.clear(); title=Table.grid(expand=True); title.add_column(justify="center")
    title.add_row("[bold cyan]N U C L E A R S H I E L D[/bold cyan]"); title.add_row("[bold]Nuclear Cybersecurity & Safety Integrity Workstation[/bold]")
    title.add_row("[dim]Schema-driven • local evidence • read-only analysis[/dim]")
    console.print(Panel(title,box=box.DOUBLE,padding=(1,2))); console.print(_status_panel()); console.print(_menu_panel())


def _run(*args: str) -> int:
    return subprocess.call([sys.executable,"-m","nuclearshield",*args],cwd=_repo_root())


def _clean_path(value: str) -> str:
    return value.strip().strip('"').strip("'").strip()


def _collect_paths() -> list[str]:
    console.print("\n[bold]Evidence selection[/bold]")
    console.print("[dim]Add one file at a time. You can also paste several paths separated by semicolons.[/dim]")
    console.print("[dim]You may drag a file from File Explorer into this window. Press Enter on an empty line when finished.[/dim]\n")
    paths: list[str] = []
    item_no = 1
    while True:
        raw = console.input(f"[bold cyan]File {item_no} > [/bold cyan]").strip()
        if not raw:
            break
        candidates = [_clean_path(item) for item in raw.split(";") if _clean_path(item)]
        for cleaned in candidates:
            candidate = Path(cleaned).expanduser()
            if not candidate.exists():
                console.print(f"[red]NOT FOUND[/red]  {cleaned}")
                console.print("[dim]Check the path. Do not use the example text 'YourName'; use your real Windows user folder or drag the file here.[/dim]")
                continue
            if not candidate.is_file():
                console.print(f"[yellow]SKIPPED[/yellow]  {cleaned}  [dim](not a file)[/dim]")
                continue
            if candidate.suffix.lower() not in SUPPORTED:
                console.print(f"[yellow]SKIPPED[/yellow]  {candidate.name}  [dim](unsupported format)[/dim]")
                continue
            resolved = str(candidate.resolve())
            if resolved not in paths:
                paths.append(resolved)
                console.print(f"[green]ADDED[/green]  {candidate.name}")
                item_no += 1
    if paths:
        console.print(f"\n[bold green]{len(paths)} evidence file(s) ready.[/bold green]")
    return paths


def _analyze(with_monitoring: bool=False) -> None:
    paths=_collect_paths()
    if not paths:
        console.print("[yellow]No valid files selected. Nothing was analyzed.[/yellow]"); return
    export=console.input("[cyan]Export JSON/TXT report after analysis? [Y/n] > [/cyan]").strip().lower()
    args=["--files",*paths]
    if export not in {"n","no"}: args.append("--export-report")
    if with_monitoring: args.extend(["--monitoring","--open-grafana"])
    _run(*args)


def main() -> None:
    while True:
        show_start_screen(); choice=console.input("\n[bold cyan]Select operation > [/bold cyan]").strip().lower()
        if choice=="1": _analyze(False); console.input("\n[dim]Press Enter to return...[/dim]")
        elif choice=="2": _analyze(True); console.input("\n[dim]Press Enter to return...[/dim]")
        elif choice=="3": webbrowser.open(GRAFANA_URL)
        elif choice=="4": webbrowser.open(PROMETHEUS_URL)
        elif choice=="5": webbrowser.open(METRICS_URL)
        elif choice=="6": _run("--self-check"); console.input("\n[dim]Press Enter to return...[/dim]")
        elif choice=="7": _run("--architecture"); _run("--assurance"); console.input("\n[dim]Press Enter to return...[/dim]")
        elif choice in {"q","quit","exit","0"}:
            console.print("[dim]NuclearShield closed. No control actions were performed.[/dim]"); return
        else:
            console.print("[yellow]Unknown selection. Choose 1-7 or Q.[/yellow]"); console.input("[dim]Press Enter to continue...[/dim]")


if __name__=="__main__": main()
