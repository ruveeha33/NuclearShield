from nuclearshield.dashboard import render_dashboard
from nuclearshield.model import FacilityState


def test_dashboard_renders_layout():
    layout = render_dashboard(FacilityState())
    assert layout["header"] is not None
    assert layout["plant"] is not None
    assert layout["threat"] is not None
