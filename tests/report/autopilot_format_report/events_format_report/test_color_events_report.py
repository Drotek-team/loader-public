import pytest
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.report import (
    ChromeInfraction,
    ColorEventsReport,
    get_report_validation,
)
from loader.shows.drone_px4.events import ColorEvents


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
    assert get_report_validation(color_events_report)


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
    assert color_events_report is not None
    assert len(color_events_report.chrome_infractions) == 1
    assert color_events_report.chrome_infractions[0] == ChromeInfraction(
        event_index=2,
        value=JSON_BINARY_PARAMETERS.chrome_value_bound.maximal + 1,
        value_min=JSON_BINARY_PARAMETERS.chrome_value_bound.minimal,
        value_max=JSON_BINARY_PARAMETERS.chrome_value_bound.maximal,
    )
