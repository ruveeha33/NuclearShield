from __future__ import annotations

from prometheus_client import Gauge, start_http_server

from .model import FacilityState

METRICS = {
    "reactor_power": Gauge("nuclearshield_reactor_power_percent", "Synthetic reactor power percentage"),
    "coolant_temp": Gauge("nuclearshield_coolant_temperature_celsius", "Synthetic coolant temperature"),
    "pressure": Gauge("nuclearshield_primary_pressure_mpa", "Synthetic primary loop pressure"),
    "neutron_flux": Gauge("nuclearshield_neutron_flux_percent", "Synthetic neutron flux percentage"),
    "safety_integrity": Gauge("nuclearshield_safety_integrity_percent", "Safety integrity score"),
    "anomaly": Gauge("nuclearshield_anomaly_score", "AI anomaly score from 0 to 1"),
    "material_delta": Gauge("nuclearshield_material_balance_delta", "Synthetic material accounting variance"),
    "access_risk": Gauge("nuclearshield_access_risk_score", "Synthetic access risk score"),
    "compliance": Gauge("nuclearshield_compliance_score_percent", "Compliance readiness score"),
    "alerts": Gauge("nuclearshield_active_alerts", "Number of active synthetic alerts"),
    "data_diode": Gauge("nuclearshield_data_diode_ok", "Simulated data diode health (1=healthy)"),
}


def start_metrics_server(port: int = 9108) -> None:
    start_http_server(port)


def update_metrics(s: FacilityState) -> None:
    METRICS["reactor_power"].set(s.reactor_power_pct)
    METRICS["coolant_temp"].set(s.coolant_temp_c)
    METRICS["pressure"].set(s.primary_pressure_mpa)
    METRICS["neutron_flux"].set(s.neutron_flux_pct)
    METRICS["safety_integrity"].set(s.safety_integrity_pct)
    METRICS["anomaly"].set(s.network_anomaly_score)
    METRICS["material_delta"].set(s.material_balance_delta)
    METRICS["access_risk"].set(s.access_risk_score)
    METRICS["compliance"].set(s.compliance_score_pct)
    METRICS["alerts"].set(s.active_alerts)
    METRICS["data_diode"].set(1 if s.data_diode_ok else 0)
