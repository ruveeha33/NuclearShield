from __future__ import annotations

from rich import box
from rich.panel import Panel
from rich.table import Table


THREAT_CONTEXT = (
    ("OT integrity", "Unexpected configuration or telemetry behavior", "Validate evidence; preserve safety boundary"),
    ("Safety assurance", "Integrity deviation in synthetic safety evidence", "Escalate to qualified human review"),
    ("Insider risk", "Unusual access combined with cyber context", "Correlate identity, access and audit evidence"),
    ("Material safeguards", "Synthetic MC&A reconciliation variance", "Initiate safeguards reconciliation review"),
    ("Supply/configuration", "Firmware or approved-baseline deviation", "Hold change; verify approved baseline"),
)

ASSURANCE_GATES = (
    ("G1", "Source / change review", "Traceable approved change request"),
    ("G2", "Automated verification", "Tests, compile checks and dashboard validation"),
    ("G3", "Configuration control", "Known baseline and drift evidence"),
    ("G4", "Safety impact review", "No weakening of independent safety functions"),
    ("G5", "Evidence release", "Audit-ready report and human authorization"),
)


def assurance_panel() -> Panel:
    table = Table(box=box.SIMPLE_HEAVY, expand=True)
    table.add_column("Gate", style="bold cyan", width=6)
    table.add_column("DevSecOps / assurance stage")
    table.add_column("Required evidence")
    for row in ASSURANCE_GATES:
        table.add_row(*row)
    return Panel(table, title="NUCLEAR SOFTWARE ASSURANCE GATES", subtitle="educational lifecycle model • no production certification", box=box.DOUBLE)


def threat_context_panel() -> Panel:
    table = Table(box=box.SIMPLE_HEAVY, expand=True)
    table.add_column("Defensive context", style="bold yellow")
    table.add_column("High-level signal")
    table.add_column("Safety-preserving disposition")
    for row in THREAT_CONTEXT:
        table.add_row(*row)
    return Panel(table, title="NUCLEAR-SECTOR DEFENSIVE THREAT CONTEXT", subtitle="no exploit procedures • no live IOC feed • synthetic educational context", box=box.DOUBLE)
