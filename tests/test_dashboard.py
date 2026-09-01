from rich.layout import Layout

from nuclearshield.dashboard import render_dashboard
from nuclearshield.model import FacilityState


def test_dashboard_builds_command_center_layout():
    layout = render_dashboard(FacilityState())
    assert isinstance(layout, Layout)
    for name in (
        "masthead",
        "core",
        "rings",
        "command",
        "risk",
        "safeguards",
        "assurance",
        "ticker",
        "footer",
    ):
        assert layout[name] is not None
