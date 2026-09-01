from __future__ import annotations

from prometheus_client import Gauge, start_http_server

from .model import FacilityState

METRICS = {
    "reactor_power": Gauge("nuclearshield_reactor_power_percent", "Synthetic reactor power percentage"),
    "coolant_temp": Gauge("nuclearshield_coolant_temperature_celsius", "Synthetic coolant temperature"),
    "pressure": Gauge("nuclearshield_primary_pressure_mpa", "Synthetic primary loop pressure"),
    "neutron_flux": Gauge("nuclearshield_neutron_flux_percent", "Synthetic neutron flux percentage"),
    "safety_integrity": Gauge("nuclearshield_safety_integrity_percent", "Synthetic safety integrity score"),
    "instrumentation_integrity": Gauge("nuclearshield_instrumentation_integrity_percent", "Synthetic instrumentation integrity score"),
    "firmware_integrity": Gauge("nuclearshield_firmware_integrity_percent", "Synthetic firmware integrity score"),
    "anomaly": Gauge("nuclearshield_anomaly_score", "AI anomaly score from 0 to 1"),
    "config_drift": Gauge("nuclearshield_configuration_drift_score", "Synthetic configuration drift score"),
    "material_delta": Gauge("nuclearshield_material_balance_delta", "Synthetic material accounting variance"),
    "access_risk": Gauge("nuclearshield_access_risk_score", "Synthetic access risk score"),
    "correlation": Gauge("nuclearshield_cyber_physical_correlation", "Synthetic cyber physical correlation score"),
    "compliance": Gauge("nuclearshield_compliance_score_percent", "Compliance readiness score"),
    "audit": Gauge("nuclearshield_audit_coverage_percent", "Synthetic audit evidence coverage"),
    "alerts": Gauge("nuclearshield_active_alerts", "Number of active synthetic alerts"),
    "enterprise_zone": Gauge("nuclearshield_enterprise_zone_ok", "Simulated enterprise/SOC zone health (1=healthy)"),
    "dmz_zone": Gauge("nuclearshield_dmz_zone_ok", "Simulated industrial DMZ health (1=healthy)"),
    "data_diode": Gauge("nuclearshield_data_diode_ok", "Simulated data diode health (1=healthy)"),
    "scada_zone": Gauge("nuclearshield_scada_zone_ok", "Simulated SCADA zone health (1=healthy)"),
    "safety_zone": Gauge("nuclearshield_safety_zone_ok", "Simulated safety zone health (1=healthy)"),
    "physical_zone": Gauge("nuclearshield_physical_security_ok", "Simulated physical security health (1=healthy)"),
    "mca_zone": Gauge("nuclearshield_material_accounting_ok", "Simulated MC&A health (1=healthy)"),
}


def start_metrics_server(port: int = 9108) -> None:
    start_http_server(port)


def update_metrics(s: FacilityState) -> None:
    METRICS["reactor_power"].set(s.reactor_power_pct)
    METRICS["coolant_temp"].set(s.coolant_temp_c)
    METRICS["pressure"].set(s.primary_pressure_mpa)
    METRICS["neutron_flux"].set(s.neutron_flux_pct)
    METRICS["safety_integrity"].set(s.safety_integrity_pct)
    METRICS["instrumentation_integrity"].set(s.instrumentation_integrity_pct)
    METRICS["firmware_integrity"].set(s.firmware_integrity_pct)
    METRICS["anomaly"].set(s.network_anomaly_score)
    METRICS["config_drift"].set(s.configuration_drift_score)
    METRICS["material_delta"].set(s.material_balance_delta)
    METRICS["access_risk"].set(s.access_risk_score)
    METRICS["correlation"].set(s.cyber_physical_correlation)
    METRICS["compliance"].set(s.compliance_score_pct)
    METRICS["audit"].set(s.audit_coverage_pct)
    METRICS["alerts"].set(s.active_alerts)
    METRICS["enterprise_zone"].set(1 if s.enterprise_zone_ok else 0)
    METRICS["dmz_zone"].set(1 if s.dmz_zone_ok else 0)
    METRICS["data_diode"].set(1 if s.data_diode_ok else 0)
    METRICS["scada_zone"].set(1 if s.scada_zone_ok else 0)
    METRICS["safety_zone"].set(1 if s.safety_zone_ok else 0)
    METRICS["physical_zone"].set(1 if s.physical_security_ok else 0)
    METRICS["mca_zone"].set(1 if s.material_accounting_ok else 0)
