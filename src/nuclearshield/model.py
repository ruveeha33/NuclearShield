from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List


@dataclass
class FacilityState:
    reactor_power_pct: float = 72.0
    coolant_temp_c: float = 286.0
    primary_pressure_mpa: float = 15.5
    neutron_flux_pct: float = 71.5
    safety_integrity_pct: float = 99.8
    network_anomaly_score: float = 0.08
    material_balance_delta: float = 0.0
    access_risk_score: float = 0.04
    data_diode_ok: bool = True
    scada_zone_ok: bool = True
    safety_zone_ok: bool = True
    physical_security_ok: bool = True
    compliance_score_pct: float = 96.0
    active_alerts: int = 0
    last_event: str = "System initialized"
    event_log: List[str] = field(default_factory=list)

    def add_event(self, message: str) -> None:
        now = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
        self.last_event = message
        self.event_log.insert(0, f"{now}  {message}")
        del self.event_log[8:]
