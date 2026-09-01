from __future__ import annotations

from rich import box
from rich.columns import Columns
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table

from .evidence import EvidencePackage


def _risk_style(score: float) -> tuple[str, str]:
    if score >= 85:
        return "bold white on red", "CRITICAL"
    if score >= 70:
        return "bold black on dark_orange", "HIGH"
    if score >= 40:
        return "bold black on yellow", "ELEVATED"
    return "bold white on green", "NORMAL"


def _bar(value: float, width: int = 18) -> str:
    value = max(0.0, min(100.0, value))
    filled = int(round((value / 100.0) * width))
    color = "green" if value < 40 else "yellow" if value < 70 else "dark_orange" if value < 85 else "red"
    return f"[{color}]" + "█" * filled + f"[/{color}][grey30]" + "░" * (width - filled) + "[/grey30]"


def _domain_card(dataset) -> Panel:
    style, label = _risk_style(dataset.anomaly_score if dataset.analyzed_rows else 0.0)
    body = Table.grid(expand=True, padding=(0, 1))
    body.add_column(style="bold cyan", width=12)
    body.add_column()
    body.add_row("DOMAIN", f"[bold]{dataset.domain}[/bold]")
    body.add_row("CONFIDENCE", f"{dataset.domain_confidence:.0f}%")
    body.add_row("RECORDS", f"{dataset.row_count:,}")
    body.add_row("FEATURES", str(len(dataset.usable_features)))
    body.add_row("MISSING", f"{dataset.missing_pct:.1f}%")
    if dataset.analyzed_rows:
        body.add_row("ANOMALY", f"{_bar(dataset.anomaly_score, 12)}  {dataset.anomaly_score:.1f}")
        body.add_row("FLAGS", str(dataset.anomaly_count))
    else:
        body.add_row("ANOMALY", "[dim]NOT MODELED[/dim]")
        body.add_row("FLAGS", "N/A")
    return Panel(body, title=f"[bold]{dataset.filename}[/bold]", subtitle=f"[{style}] {label} [/] ", box=box.ROUNDED, border_style="cyan")


def render_command_center(package: EvidencePackage, console: Console | None = None) -> None:
    console = console or Console()
    console.clear()
    risk_style, risk_label = _risk_style(package.overall_risk_score)

    header = Table.grid(expand=True)
    header.add_column(justify="center")
    header.add_row("[bold bright_cyan]⚛  N U C L E A R S H I E L D  ⚛[/bold bright_cyan]")
    header.add_row("[bold white]NUCLEAR CYBER DEFENSE COMMAND CENTER[/bold white]")
    header.add_row("[dim]Evidence-driven • local • read-only • schema-adaptive[/dim]")
    console.print(Panel(header, box=box.DOUBLE, border_style="bright_cyan", padding=(1, 2)))

    stats = Table.grid(expand=True, padding=(0, 1))
    for _ in range(5):
        stats.add_column(ratio=1)
    total_flags = sum(d.anomaly_count for d in package.datasets if d.analyzed_rows)
    avg_missing = sum(d.missing_pct for d in package.datasets) / max(1, len(package.datasets))
    stats.add_row(
        Panel(f"[bold bright_cyan]{len(package.datasets)}[/bold bright_cyan]\n[dim]EVIDENCE SOURCES[/dim]", border_style="blue", box=box.ROUNDED),
        Panel(f"[bold magenta]{package.total_rows:,}[/bold magenta]\n[dim]RECORDS INDEXED[/dim]", border_style="magenta", box=box.ROUNDED),
        Panel(f"[{risk_style}]{package.overall_risk_score:.1f}/100[/]\n[dim]CROSS-FILE RISK[/dim]", border_style="yellow" if package.overall_risk_score >= 40 else "green", box=box.ROUNDED),
        Panel(f"[bold yellow]{total_flags:,}[/bold yellow]\n[dim]MODEL FLAGS[/dim]", border_style="yellow", box=box.ROUNDED),
        Panel(f"[bold green]{100-avg_missing:.1f}%[/bold green]\n[dim]DATA QUALITY[/dim]", border_style="green", box=box.ROUNDED),
    )
    console.print(stats)

    risk = Table.grid(expand=True, padding=(0, 2))
    risk.add_column(ratio=2)
    risk.add_column(ratio=1)
    risk.add_row(
        Panel(
            f"[bold]GLOBAL ANOMALY PRESSURE[/bold]\n\n{_bar(package.overall_risk_score, 32)}  [bold]{package.overall_risk_score:.1f}/100[/bold]\n\n"
            f"[{risk_style}] {risk_label} [/]   [dim]Derived from loaded evidence only[/dim]",
            border_style="bright_blue", box=box.HEAVY,
        ),
        Panel(
            "[bold green]● ANALYSIS ENGINE ONLINE[/bold green]\n"
            "[green]● LOCAL EVIDENCE LOADED[/green]\n"
            "[green]● CONTROL WRITES DISABLED[/green]\n"
            "[cyan]● HUMAN REVIEW REQUIRED[/cyan]",
            title="PLATFORM STATUS", border_style="green", box=box.HEAVY,
        ),
    )
    console.print(risk)

    cards = [_domain_card(dataset) for dataset in package.datasets]
    console.print(Columns(cards, equal=True, expand=True, column_first=False))

    ranking = sorted(package.datasets, key=lambda d: d.anomaly_score if d.analyzed_rows else -1, reverse=True)
    risk_table = Table(box=box.SIMPLE_HEAVY, expand=True)
    risk_table.add_column("PRIORITY", style="bold")
    risk_table.add_column("DOMAIN")
    risk_table.add_column("ANOMALY PRESSURE")
    risk_table.add_column("FLAGS", justify="right")
    risk_table.add_column("SOURCE")
    for i, d in enumerate(ranking, start=1):
        score = d.anomaly_score if d.analyzed_rows else 0.0
        risk_table.add_row(f"#{i}", d.domain, f"{_bar(score, 14)} {score:.1f}", str(d.anomaly_count) if d.analyzed_rows else "N/A", d.filename)

    workflow = Panel(
        "[bright_cyan]LOCAL FILES[/bright_cyan]  →  [cyan]SCHEMA PROFILING[/cyan]  →  [magenta]FEATURE DISCOVERY[/magenta]  →  "
        "[yellow]AI ANOMALY ANALYSIS[/yellow]  →  [orange3]CROSS-FILE RISK[/orange3]  →  [green]HUMAN REVIEW[/green]\n\n"
        "[dim]No evidence → no metric → no fabricated finding. No PLC/reactor control path is implemented.[/dim]",
        title="DEFENSE-IN-DEPTH ANALYSIS PIPELINE", border_style="bright_cyan", box=box.ROUNDED,
    )
    console.print(Group(Panel(risk_table, title="EVIDENCE PRIORITY QUEUE", border_style="magenta", box=box.ROUNDED), workflow))
