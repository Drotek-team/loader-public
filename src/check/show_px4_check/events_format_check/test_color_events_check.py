import pytest

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ....show_env.show_px4.drone_px4.events.color_events import ColorEvents
from .events_format_check_procedure import color_events_check


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


def test_valid_color_events_check(
    valid_color_events: ColorEvents,
):
    color_events_check(
        valid_color_events,
    )


def test_invalid_color_events_frame_increasing_check(
    valid_color_events: ColorEvents,
):
    valid_color_events.add_timecode_rgbw(
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        ),
        (0, 0, 0, 0),
    )
    color_events_contenor = color_events_check(
        valid_color_events,
    )
    assert not color_events_contenor["Frame check"]["Increasing"].user_validation


def test_invalid_color_events_frame_first_frame_check(
    valid_color_events: ColorEvents,
):
    valid_color_events.add_timecode_rgbw(
        timecode=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        )
        - 1,
        rgbw=(0, 0, 0, 0),
    )
    color_events_contenor = color_events_check(
        valid_color_events,
    )
    assert not (color_events_contenor["Frame check"]["Value"].user_validation)


def test_invalid_color_events_rgbw_value_check(
    valid_color_events: ColorEvents,
):
    valid_color_events.add_timecode_rgbw(
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        ),
        (JSON_BINARY_PARAMETER.color_value_max + 1, 0, 0, 0),
    )
    color_events_contenor = color_events_check(
        valid_color_events,
    )
    assert not (color_events_contenor["Rgbw check"]["Value"].user_validation)
