from __future__ import annotations

import math
import random
from collections import deque

import numpy as np
from sklearn.ensemble import IsolationForest

from .model import FacilityState


SCENARIOS = {
    "normal": "Baseline defensive monitoring",
    "scada-anomaly": "Synthetic OT/SCADA communication anomaly",
    "safety-integrity": "Synthetic safety instrumentation integrity deviation",
    "insider-risk": "Synthetic physical-cyber access risk correlation",
    "material-variance": "Synthetic MC&A variance requiring safeguards review",
    "combined": "Rotating multi-domain exam demonstration",
}


class FacilitySimulator:
    """Generates synthetic defensive telemetry only; never touches real OT systems."""

    def __init__(self, scenario: str = "normal", seed: int | None = None) -> None:
        if scenario not in SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario}")
        self.scenario = scenario
        self.random = random.Random(seed)
        self.tick_count = 0
        self.history: deque[list[float]] = deque(maxlen=180)
        self.detector = IsolationForest(contamination=0.06, random_state=42)
        self.detector_ready = False

    def _features(self, s: FacilityState) -> list[float]:
        return [
            s.reactor_power_pct,
            s.coolant_temp_c,
            s.primary_pressure_mpa,
            s.neutron_flux_pct,
            s.instrumentation_integrity_pct,
            s.material_balance_delta,
            s.access_risk_score,
            s.configuration_drift_score,
        ]

    def _maybe_fit(self) -> None:
        if len(self.history) >= 30 and self.tick_count % 12 == 0:
            self.detector.fit(np.asarray(self.history, dtype=float))
            self.detector_ready = True

    def _active_scenario(self) -> str:
        if self.scenario != "combined":
            return self.scenario
        cycle = (self.tick_count // 18) % 5
        return ["normal", "scada-anomaly", "safety-integrity", "insider-risk", "material-variance"][cycle]

    def step(self, state: FacilityState) -> FacilityState:
        self.tick_count += 1
        state.tick = self.tick_count
        scenario = self._active_scenario()
        state.scenario = scenario
        phase = self.tick_count / 9.0

        # Baseline synthetic behavior; values are illustrative, not operating guidance.
        state.reactor_power_pct = 72 + math.sin(phase) * 1.4 + self.random.uniform(-0.25, 0.25)
        state.coolant_temp_c = 286 + math.sin(phase / 1.8) * 0.9 + self.random.uniform(-0.18, 0.18)
        state.primary_pressure_mpa = 15.5 + math.sin(phase / 2.2) * 0.06 + self.random.uniform(-0.018, 0.018)
        state.neutron_flux_pct = state.reactor_power_pct - 0.35 + self.random.uniform(-0.22, 0.22)
        state.instrumentation_integrity_pct = 99.75 + self.random.uniform(-0.08, 0.08)
        state.firmware_integrity_pct = 99.92 + self.random.uniform(-0.03, 0.03)
        state.material_balance_delta = max(0.0, self.random.gauss(0.0, 0.008))
        state.access_risk_score = max(0.01, min(1.0, self.random.gauss(0.05, 0.015)))
        state.configuration_drift_score = max(0.01, min(1.0, self.random.gauss(0.04, 0.012)))
        state.cyber_physical_correlation = max(0.01, min(1.0, self.random.gauss(0.05, 0.015)))

        state.enterprise_zone_ok = True
        state.dmz_zone_ok = True
        state.scada_zone_ok = True
        state.safety_zone_ok = True
        state.physical_security_ok = True
        state.material_accounting_ok = True
        state.data_diode_ok = True

        # Scenario injections are intentionally descriptive and non-actionable.
        if scenario == "scada-anomaly" and self.tick_count % 6 in {0, 1, 2}:
            state.configuration_drift_score = 0.68
            state.cyber_physical_correlation = 0.61
            state.scada_zone_ok = False
            if self.tick_count % 6 == 0:
                state.add_event("Synthetic OT communication pattern departed from baseline; monitoring zone flagged", "OT")

        if scenario == "safety-integrity" and self.tick_count % 7 in {0, 1}:
            state.instrumentation_integrity_pct = 96.8
            state.coolant_temp_c += 4.2
            state.safety_zone_ok = False
            if self.tick_count % 7 == 0:
                state.add_event("Synthetic safety-channel integrity deviation detected; independent safety boundary preserved", "SAFETY")

        if scenario == "insider-risk" and self.tick_count % 6 in {0, 1, 2}:
            state.access_risk_score = 0.78
            state.cyber_physical_correlation = 0.73
            state.physical_security_ok = False
            if self.tick_count % 6 == 0:
                state.add_event("Synthetic badge/session behavior correlation requires human identity review", "ACCESS")

        if scenario == "material-variance" and self.tick_count % 8 in {0, 1, 2}:
            state.material_balance_delta = 0.145
            state.material_accounting_ok = False
            if self.tick_count % 8 == 0:
                state.add_event("Synthetic MC&A reconciliation variance queued for safeguards review", "MC&A")

        self.history.append(self._features(state))
        self._maybe_fit()

        if self.detector_ready:
            sample = np.asarray([self._features(state)], dtype=float)
            decision = float(self.detector.decision_function(sample)[0])
            state.network_anomaly_score = max(0.0, min(1.0, 0.48 - decision * 2.4))
        else:
            state.network_anomaly_score = min(
                0.65,
                0.05 + 0.40 * state.configuration_drift_score + 0.20 * state.access_risk_score,
            )

        safety_risk = max(0.0, min(1.0, (99.8 - state.instrumentation_integrity_pct) / 4.0))
        material_risk = min(1.0, state.material_balance_delta / 0.16)
        fused = max(
            state.network_anomaly_score,
            state.access_risk_score,
            state.configuration_drift_score,
            state.cyber_physical_correlation,
            safety_risk,
            material_risk,
        )

        if fused >= 0.75:
            state.risk_level = "CRITICAL"
            state.response_mode = "SAFETY-PRESERVING REVIEW"
        elif fused >= 0.55:
            state.risk_level = "HIGH"
            state.response_mode = "HUMAN TRIAGE"
        elif fused >= 0.30:
            state.risk_level = "ELEVATED"
            state.response_mode = "ENHANCED MONITORING"
        else:
            state.risk_level = "NORMAL"
            state.response_mode = "MONITOR"

        state.active_alerts = sum(
            [
                state.network_anomaly_score > 0.55,
                state.access_risk_score > 0.55,
                state.material_balance_delta > 0.10,
                state.instrumentation_integrity_pct < 98.0,
                state.configuration_drift_score > 0.55,
            ]
        )
        state.safety_integrity_pct = max(96.0, min(99.95, state.instrumentation_integrity_pct + 0.10))
        state.audit_coverage_pct = 98.4 if state.active_alerts == 0 else 97.2
        state.compliance_score_pct = 97.6 if state.active_alerts == 0 else max(91.0, 97.6 - state.active_alerts * 1.4)
        return state
