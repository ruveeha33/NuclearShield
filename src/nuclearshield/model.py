from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class FacilityState:
    """Synthetic state for the classroom-only NuclearShield digital facility."""

    scenario: str = "normal"
    tick: int = 0

    # Illustrative plant/safety signals. These are not real plant set-points.
    reactor_power_pct: float = 72.0
    coolant_temp_c: float = 286.0
    primary_pressure_mpa: float = 15.5
    neutron_flux_pct: float = 71.5
    safety_integrity_pct: float = 99.8
    instrumentation_integrity_pct: float = 99.7
    firmware_integrity_pct: float = 99.9

    # Defensive cyber / safeguards signals.
    network_anomaly_score: float = 0.08
    access_risk_score: float = 0.04
    material_balance_delta: float = 0.0
    configuration_drift_score: float = 0.03
    cyber_physical_correlation: float = 0.05

    data_diode_ok: bool = True
    enterprise_zone_ok: bool = True
    dmz_zone_ok: bool = True
    scada_zone_ok: bool = True
    safety_zone_ok: bool = True
    physical_security_ok: bool = True
    material_accounting_ok: bool = True

    compliance_score_pct: float = 97.0
    audit_coverage_pct: float = 98.0
    active_alerts: int = 0
    response_mode: str = "MONITOR"
    risk_level: str = "NORMAL"

    last_event: str = "System initialized"
    event_log: List[str] = field(default_factory=list)

    def add_event(self, message: str, category: str = "SYSTEM") -> None:
        now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
        self.last_event = message
        self.event_log.insert(0, f"{now}  [{category}] {message}")
        del self.event_log[7:]
