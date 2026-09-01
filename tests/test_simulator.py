from nuclearshield.model import FacilityState
from nuclearshield.simulator import FacilitySimulator


def test_simulator_keeps_values_in_reasonable_synthetic_ranges():
    state = FacilityState()
    sim = FacilitySimulator(seed=7)
    for _ in range(25):
        sim.step(state)
    assert 60 < state.reactor_power_pct < 85
    assert 270 < state.coolant_temp_c < 305
    assert 14 < state.primary_pressure_mpa < 17
    assert 0 <= state.network_anomaly_score <= 1
    assert 0 <= state.access_risk_score <= 1
    assert state.safety_integrity_pct >= 99
