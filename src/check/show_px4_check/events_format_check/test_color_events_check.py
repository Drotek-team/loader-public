import pytest

from ....migration.show_px4.drone_px4.events.color_events import ColorEvent, ColorEvents
from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from .events_format_check_procedure import color_events_check
from .events_format_check_report import ColorEventsCheckReport


@pytest.fixture
def valid_color_events():
    color_events = ColorEvents()
    color_events.add_timecode_rgbw(
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        ),
        (0, 0, 0, 0),
    )
    color_events.add_timecode_rgbw(
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        )
        + 1,
        (255, 255, 255, 255),
    )
    return color_events


@pytest.fixture
def color_events_check_report():
    return ColorEventsCheckReport()


def test_valid_color_events_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    color_events_check(
        valid_color_events,
        color_events_check_report,
    )


def test_invalid_color_events_frame_increasing_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    valid_color_events.add_timecode_rgbw(
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        ),
        (0, 0, 0, 0),
    )
    color_events_check(
        valid_color_events,
        color_events_check_report,
    )
    assert not (
        color_events_check_report.frame_check_report.increasing_frame_check_report.validation
    )


def test_invalid_color_events_frame_first_frame_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    valid_color_events.events.insert(
        0,
        ColorEvent(
            FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                JSON_BINARY_PARAMETER.show_duration_min_second
            )
            - 1,
            0,
            0,
            0,
            0,
        ),
    )
    color_events_check(
        valid_color_events,
        color_events_check_report,
    )
    assert not (
        color_events_check_report.frame_check_report.frame_value_check_report.validation
    )


def test_invalid_color_events_rgbw_value_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    valid_color_events.add_timecode_rgbw(
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        ),
        (JSON_BINARY_PARAMETER.color_value_max + 1, 0, 0, 0),
    )
    color_events_check(
        valid_color_events,
        color_events_check_report,
    )
    assert not (
        color_events_check_report.rgbw_check_report.rgbw_value_check_report.validation
    )
