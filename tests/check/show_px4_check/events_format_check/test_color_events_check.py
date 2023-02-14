import pytest
from loader.check.show_px4_check.events_format_check import (
    IntegerBoundaryInfraction,
    get_color_events_report,
)
from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.report import get_base_report_validation
from loader.show_env.show_px4.drone_px4.events.color_events import ColorEvents


@pytest.fixture
def valid_color_events() -> ColorEvents:
    color_events = ColorEvents()
    color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame,
        ),
        (0, 0, 0, 0),
    )
    color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame + 1,
        ),
        (
            JSON_BINARY_PARAMETER.chrome_value_bound.minimal,
            JSON_BINARY_PARAMETER.chrome_value_bound.minimal,
            JSON_BINARY_PARAMETER.chrome_value_bound.maximal,
            JSON_BINARY_PARAMETER.chrome_value_bound.maximal,
        ),
    )
    return color_events


def test_valid_color_events_check(
    valid_color_events: ColorEvents,
) -> None:
    color_events_report = get_color_events_report(
        valid_color_events,
    )
    assert get_base_report_validation(color_events_report)


def test_invalid_color_events_rgbw_value_check(
    valid_color_events: ColorEvents,
) -> None:
    valid_color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame + 2,
        ),
        (JSON_BINARY_PARAMETER.chrome_value_bound.maximal + 1, 0, 0, 0),
    )
    color_events_report = get_color_events_report(
        valid_color_events,
    )
    if color_events_report is None:
        msg = "color_events_report is None"
        raise ValueError(msg)
    assert len(color_events_report.chrome_infractions) == 1
    assert (
        color_events_report.chrome_infractions[0].dict()
        == IntegerBoundaryInfraction(
            data_type="chrome",
            event_index=2,
            value=JSON_BINARY_PARAMETER.chrome_value_bound.maximal + 1,
            value_min=JSON_BINARY_PARAMETER.chrome_value_bound.minimal,
            value_max=JSON_BINARY_PARAMETER.chrome_value_bound.maximal,
        ).dict()
    )
