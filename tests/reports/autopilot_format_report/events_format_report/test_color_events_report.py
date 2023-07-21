import pytest
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.reports import ColorBoundaryInfraction, ColorEventsReport
from loader.schemas.drone_px4.events import ColorEvents


@pytest.fixture
def valid_color_events() -> ColorEvents:
    color_events = ColorEvents()
    color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETERS.show_start_frame,
        ),
        (0, 0, 0, 0),
    )
    color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETERS.show_start_frame + 1,
        ),
        (
            JSON_BINARY_PARAMETERS.chrome_value_bound.minimal,
            JSON_BINARY_PARAMETERS.chrome_value_bound.minimal,
            JSON_BINARY_PARAMETERS.chrome_value_bound.maximal,
            JSON_BINARY_PARAMETERS.chrome_value_bound.maximal,
        ),
    )
    return color_events


def test_valid_color_events_report(
    valid_color_events: ColorEvents,
) -> None:
    color_events_report = ColorEventsReport.generate(
        valid_color_events,
    )
    assert not len(color_events_report)


def test_invalid_color_events_rgbw_value_report(
    valid_color_events: ColorEvents,
) -> None:
    valid_color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETERS.show_start_frame + 2,
        ),
        (JSON_BINARY_PARAMETERS.chrome_value_bound.maximal + 1, 0, 0, 0),
    )
    color_events_report = ColorEventsReport.generate(
        valid_color_events,
    )
    assert len(color_events_report)
    assert len(color_events_report.color_infractions) == 1
    assert color_events_report.color_infractions[0] == ColorBoundaryInfraction(
        event_index=2,
        channel="red",
        value=JSON_BINARY_PARAMETERS.chrome_value_bound.maximal + 1,
    )
