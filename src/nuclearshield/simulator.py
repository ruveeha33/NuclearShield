from __future__ import annotations

import math
import random
import time
from collections import deque

import numpy as np
from sklearn.ensemble import IsolationForest

from .model import FacilityState


class FacilitySimulator:
    """Generates synthetic plant/security telemetry only; never touches real OT systems."""

    def __init__(self, seed: int | None = None) -> None:
        self.random = random.Random(seed)
        self.tick_count = 0
        self.history = deque(maxlen=120)
        self.detector = IsolationForest(contamination=0.08, random_state=42)
        self.detector_ready = False

    def _features(self, s: FacilityState) -> list[float]:
        return [
            s.reactor_power_pct,
            s.coolant_temp_c,
            s.primary_pressure_mpa,
            s.neutron_flux_pct,
            s.material_balance_delta,
            s.access_risk_score,
        ]

    def _maybe_fit(self) -> None:
        if len(self.history) >= 30 and self.tick_count % 15 == 0:
            x = np.asarray(self.history, dtype=float)
            self.detector.fit(x)
            self.detector_ready = True

    def step(self, state: FacilityState) -> FacilityState:
        self.tick_count += 1
        phase = self.tick_count / 10.0

        state.reactor_power_pct = 72 + math.sin(phase) * 1.8 + self.random.uniform(-0.35, 0.35)
        state.coolant_temp_c = 286 + math.sin(phase / 1.7) * 1.2 + self.random.uniform(-0.25, 0.25)
        state.primary_pressure_mpa = 15.5 + math.sin(phase / 2.0) * 0.08 + self.random.uniform(-0.025, 0.025)
        state.neutron_flux_pct = state.reactor_power_pct - 0.4 + self.random.uniform(-0.3, 0.3)
        state.material_balance_delta = max(0.0, self.random.gauss(0.0, 0.012))
        state.access_risk_score = max(0.01, min(1.0, self.random.gauss(0.05, 0.02)))

        # Rare, synthetic anomalies for demonstration.
        if self.tick_count % 37 == 0:
            state.access_risk_score = 0.76
            state.add_event("Synthetic access anomaly detected; identity session isolated")
        if self.tick_count % 53 == 0:
            state.material_balance_delta = 0.16
            state.add_event("Synthetic MC&A variance flagged for manual review")
        if self.tick_count % 71 == 0:
            state.coolant_temp_c += 7.5
            state.add_event("Synthetic instrumentation deviation detected; safety channel preserved")

        self.history.append(self._features(state))
        self._maybe_fit()

        if self.detector_ready:
            sample = np.asarray([self._features(state)], dtype=float)
            decision = float(self.detector.decision_function(sample)[0])
            state.network_anomaly_score = max(0.0, min(1.0, 0.5 - decision))
        else:
            state.network_anomaly_score = min(0.45, 0.06 + state.access_risk_score * 0.25)

        state.active_alerts = sum(
            [
                state.network_anomaly_score > 0.45,
                state.access_risk_score > 0.55,
                state.material_balance_delta > 0.10,
                state.coolant_temp_c > 291.0,
            ]
        )
        state.safety_integrity_pct = 99.9 if state.coolant_temp_c < 291 else 99.2
        state.compliance_score_pct = 97.0 if state.active_alerts == 0 else 94.0
        return state

    def run_delay(self, seconds: float = 1.0) -> None:
        time.sleep(seconds)
