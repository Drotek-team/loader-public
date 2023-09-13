import pytest
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, MagicNumber
from loader.reports import BoundaryInfraction, EventsReport
from loader.schemas.drone_px4.events import ColorEvents


@pytest.fixture
def valid_color_events(request: pytest.FixtureRequest) -> ColorEvents:
    color_events = ColorEvents(request.param)
    color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETERS.show_start_frame,
        (0, 0, 0, 0),
    )
    color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETERS.show_start_frame + 1,
        (
            JSON_BINARY_PARAMETERS.chrome_value_bound.minimal,
            JSON_BINARY_PARAMETERS.chrome_value_bound.minimal,
            JSON_BINARY_PARAMETERS.chrome_value_bound.maximal,
            JSON_BINARY_PARAMETERS.chrome_value_bound.maximal,
        ),
    )
    return color_events


@pytest.mark.parametrize("valid_color_events", list(MagicNumber), indirect=True)
def test_valid_color_events_report(
    valid_color_events: ColorEvents,
) -> None:
    color_events_report = EventsReport.generate(
        valid_color_events,
    )
    assert not len(color_events_report)


@pytest.mark.parametrize("valid_color_events", list(MagicNumber), indirect=True)
def test_invalid_color_events_rgbw_value_report(
    valid_color_events: ColorEvents,
) -> None:
    valid_color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETERS.show_start_frame + 2,
        (JSON_BINARY_PARAMETERS.chrome_value_bound.maximal + 1, 0, 0, 0),
    )
    color_events_report = EventsReport.generate(
        valid_color_events,
    )
    assert len(color_events_report)
    assert len(color_events_report.boundary_infractions) == 1
    assert color_events_report.boundary_infractions["red"][0] == BoundaryInfraction(
        event_index=2,
        value=JSON_BINARY_PARAMETERS.chrome_value_bound.maximal + 1,
    )
