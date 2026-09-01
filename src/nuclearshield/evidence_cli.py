from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .assurance import assurance_panel, threat_context_panel
from .evidence import EvidencePackage, SUPPORTED_EXTENSIONS, analyze_files

console = Console()


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def show_architecture() -> None:
    console.print(Panel.fit(
        "USER-SUPPLIED EVIDENCE FILES\n"
        "          ↓\n"
        "SCHEMA PROFILING + DATA VALIDATION\n"
        "          ↓\n"
        "DOMAIN INFERENCE + FEATURE DISCOVERY\n"
        "          ↓\n"
        "DATA-DRIVEN ANOMALY ANALYSIS\n"
        "          ↓\n"
        "CROSS-FILE EVIDENCE SUMMARY\n"
        "          ↓\n"
        "HUMAN REVIEW + READ-ONLY REPORTING",
        title="NuclearShield Evidence Analysis Architecture",
        subtitle="No fixed filenames • no automatic scenario • no control path",
        box=box.DOUBLE,
    ))


def system_check() -> int:
    checks = [
        ("Python runtime", True, "available"),
        ("Evidence engine", True, "schema-driven ingestion enabled"),
        ("CSV / JSON", True, "built-in readers"),
        ("XLSX reader", _has_openpyxl(), "openpyxl"),
        ("Docker CLI", shutil.which("docker") is not None, "optional browser monitoring"),
    ]
    table = Table(title="NUCLEARSHIELD READINESS CHECK", box=box.SIMPLE_HEAVY)
    table.add_column("Component")
    table.add_column("State", justify="center")
    table.add_column("Purpose")
    for name, ok, purpose in checks:
        table.add_row(name, "[bold green]READY[/bold green]" if ok else "[yellow]OPTIONAL / MISSING[/yellow]", purpose)
    console.print(table)
    return 0 if all(ok for name, ok, _ in checks if name != "Docker CLI") else 1


def _has_openpyxl() -> bool:
    try:
        import openpyxl  # noqa: F401
        return True
    except ImportError:
        return False


def render_package(package: EvidencePackage) -> Panel:
    table = Table(expand=True, box=box.SIMPLE_HEAVY)
    table.add_column("File", ratio=3)
    table.add_column("Detected domain", ratio=2)
    table.add_column("Rows", justify="right")
    table.add_column("Numeric features", justify="right")
    table.add_column("Missing", justify="right")
    table.add_column("Anomaly pressure", justify="right")
    table.add_column("Model flags", justify="right")

    for dataset in package.datasets:
        domain = dataset.domain
        if dataset.domain_confidence > 0:
            domain += f"\n[dim]{dataset.domain_confidence:.0f}% schema confidence[/dim]"
        table.add_row(
            dataset.filename,
            domain,
            f"{dataset.row_count:,}",
            str(len(dataset.usable_features)),
            f"{dataset.missing_pct:.1f}%",
            f"{dataset.anomaly_score:.1f}/100" if dataset.analyzed_rows else "N/A",
            str(dataset.anomaly_count) if dataset.analyzed_rows else "N/A",
        )

    summary = Table.grid(expand=True, padding=(0, 2))
    summary.add_column(style="bold cyan")
    summary.add_column(justify="right")
    summary.add_row("Evidence files", str(len(package.datasets)))
    summary.add_row("Records indexed", f"{package.total_rows:,}")
    summary.add_row("Cross-file risk", f"{package.overall_risk_score:.1f}/100")
    summary.add_row("Assessment", package.risk_level)

    body = Table.grid(expand=True)
    body.add_row(summary)
    body.add_row(table)
    return Panel(
        body,
        title="NUCLEARSHIELD // EVIDENCE ANALYSIS",
        subtitle="Analysis is derived only from supplied files; no missing domain is fabricated",
        box=box.DOUBLE,
    )


def render_details(package: EvidencePackage) -> None:
    for index, dataset in enumerate(package.datasets, start=1):
        details = Table.grid(expand=True, padding=(0, 1))
        details.add_column(style="bold cyan", width=20)
        details.add_column()
        details.add_row("FILE", f"{index:02d}  {dataset.filename}")
        details.add_row("DETECTED DOMAIN", dataset.domain)
        details.add_row("SCHEMA CONFIDENCE", f"{dataset.domain_confidence:.1f}%" if dataset.domain_confidence else "INSUFFICIENT")
        details.add_row("ROWS", f"{dataset.row_count:,}")
        details.add_row("COLUMNS", ", ".join(dataset.columns[:12]) + (" ..." if len(dataset.columns) > 12 else ""))
        details.add_row("NUMERIC FEATURES", ", ".join(dataset.usable_features[:10]) or "None suitable")
        details.add_row("TIMESTAMP", dataset.timestamp_column or "Not detected")
        details.add_row("MISSING DATA", f"{dataset.missing_pct:.2f}%")
        details.add_row("ANOMALY PRESSURE", f"{dataset.anomaly_score:.1f}/100" if dataset.analyzed_rows else "Not modeled")
        details.add_row("FLAGGED ROWS", str(dataset.anomaly_count) if dataset.analyzed_rows else "N/A")
        if dataset.notes:
            details.add_row("NOTES", " | ".join(dataset.notes))
        console.print(Panel(details, title=f"EVIDENCE SOURCE {index:02d}", box=box.ROUNDED))


def export_report(package: EvidencePackage, destination: Path | None = None) -> tuple[Path, Path]:
    destination = destination or (_repo_root() / "reports")
    destination.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    json_path = destination / f"nuclearshield-evidence-{stamp}.json"
    txt_path = destination / f"nuclearshield-evidence-{stamp}.txt"
    payload = {
        "title": "NuclearShield Evidence Analysis",
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "data_policy": "Derived only from user-supplied local evidence files",
        "files": len(package.datasets),
        "total_rows": package.total_rows,
        "overall_risk_score": round(package.overall_risk_score, 2),
        "risk_level": package.risk_level,
        "datasets": [
            {
                "file": dataset.filename,
                "domain": dataset.domain,
                "domain_confidence": round(dataset.domain_confidence, 2),
                "rows": dataset.row_count,
                "columns": dataset.columns,
                "numeric_features": dataset.usable_features,
                "timestamp_column": dataset.timestamp_column,
                "missing_pct": round(dataset.missing_pct, 3),
                "anomaly_score": round(dataset.anomaly_score, 2),
                "anomaly_count": dataset.anomaly_count,
                "analyzed_rows": dataset.analyzed_rows,
                "notes": dataset.notes,
            }
            for dataset in package.datasets
        ],
        "safety_boundary": "Read-only offline analysis; NuclearShield has no industrial or facility control capability.",
    }
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "NUCLEARSHIELD EVIDENCE ANALYSIS",
        "=" * 72,
        f"Files: {len(package.datasets)}",
        f"Rows: {package.total_rows}",
        f"Cross-file risk: {package.overall_risk_score:.1f}/100 ({package.risk_level})",
        "",
    ]
    for dataset in package.datasets:
        lines.extend([
            dataset.filename,
            f"  Domain: {dataset.domain} ({dataset.domain_confidence:.1f}% schema confidence)",
            f"  Rows: {dataset.row_count}",
            f"  Numeric features: {', '.join(dataset.usable_features) or 'none'}",
            f"  Missing: {dataset.missing_pct:.2f}%",
            f"  Anomaly pressure: {dataset.anomaly_score:.1f}/100" if dataset.analyzed_rows else "  Anomaly pressure: not modeled",
            f"  Flagged rows: {dataset.anomaly_count}" if dataset.analyzed_rows else "  Flagged rows: N/A",
            "",
        ])
    lines.append("Safety boundary: read-only offline analysis; no industrial or facility control capability.")
    txt_path.write_text("\n".join(lines), encoding="utf-8")
    return json_path, txt_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="NuclearShield schema-driven defensive evidence analyzer")
    parser.add_argument("--files", nargs="+", help="one or more local CSV, JSON, JSONL, or XLSX evidence files")
    parser.add_argument("--export-report", action="store_true", help="export JSON and text analysis reports")
    parser.add_argument("--self-check", action="store_true", help="check local analysis prerequisites")
    parser.add_argument("--architecture", action="store_true", help="show the evidence-analysis architecture")
    parser.add_argument("--assurance", action="store_true", help="show defensive software assurance gates")
    parser.add_argument("--threat-context", action="store_true", help="show safe high-level defensive threat context")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.self_check:
        raise SystemExit(system_check())
    if args.architecture:
        show_architecture(); return
    if args.assurance:
        console.print(assurance_panel()); return
    if args.threat_context:
        console.print(threat_context_panel()); return
    if not args.files:
        supported = ", ".join(sorted(SUPPORTED_EXTENSIONS))
        console.print(Panel.fit(
            f"[bold]NO EVIDENCE PACKAGE LOADED[/bold]\n\n"
            f"Supply one or more local evidence files to begin analysis.\n"
            f"Supported formats: {supported}\n\n"
            f"Example:\n  python -m nuclearshield --files file_a.csv file_b.xlsx",
            title="NUCLEARSHIELD",
            subtitle="No data → no analysis → no fabricated findings",
            box=box.DOUBLE,
        ))
        return

    try:
        package = analyze_files(args.files)
    except (FileNotFoundError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        console.print(f"[bold red]Evidence ingestion failed:[/bold red] {exc}")
        raise SystemExit(2) from exc

    console.print(render_package(package))
    render_details(package)
    if args.export_report:
        json_path, txt_path = export_report(package)
        console.print(f"[cyan]Analysis exported:[/cyan] {json_path.name} | {txt_path.name}")


if __name__ == "__main__":
    main()
