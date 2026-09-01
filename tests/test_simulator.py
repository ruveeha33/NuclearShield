from nuclearshield.model import FacilityState
from nuclearshield.simulator import FacilitySimulator, SCENARIOS


def test_simulator_keeps_scores_bounded():
    state = FacilityState()
    sim = FacilitySimulator(seed=1)
    for _ in range(40):
        sim.step(state)
    assert 0 <= state.network_anomaly_score <= 1
    assert 0 <= state.access_risk_score <= 1
    assert 0 <= state.configuration_drift_score <= 1
    assert 90 <= state.compliance_score_pct <= 100
    assert state.tick == 40


def test_all_scenarios_run():
    for scenario in SCENARIOS:
        state = FacilityState()
        sim = FacilitySimulator(scenario=scenario, seed=132)
        for _ in range(20):
            sim.step(state)
        assert state.risk_level in {"NORMAL", "ELEVATED", "HIGH", "CRITICAL"}
        assert state.response_mode


def test_material_scenario_can_flag_mca():
    state = FacilityState()
    sim = FacilitySimulator(scenario="material-variance", seed=132)
    for _ in range(8):
        sim.step(state)
    assert state.material_balance_delta >= 0.10
    assert not state.material_accounting_ok
