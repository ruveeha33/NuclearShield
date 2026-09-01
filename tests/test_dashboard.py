from rich.layout import Layout

from nuclearshield.dashboard import render_dashboard
from nuclearshield.model import FacilityState


def test_dashboard_builds_soc_layout():
    layout = render_dashboard(FacilityState())
    assert isinstance(layout, Layout)
    assert layout["header"] is not None
    assert layout["facility"] is not None
    assert layout["safety"] is not None
    assert layout["ot"] is not None
    assert layout["risk"] is not None
    assert layout["material"] is not None
    assert layout["events"] is not None
