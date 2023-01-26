import pytest

from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ....show_env.show_px4.drone_px4.events.color_events import ColorEvents
from .events_format_check_procedure import color_events_check


@pytest.fixture
def valid_color_events():
    color_events = ColorEvents()
    color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame
        ),
        (0, 0, 0, 0),
    )
    color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame + 1
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
):
    color_events_contenor = color_events_check(
        valid_color_events,
    )
    assert color_events_contenor.user_validation


def test_invalid_color_events_frame_increasing_check(
    valid_color_events: ColorEvents,
):
    valid_color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETER.show_start_frame,
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
        timecode=JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame - 1
        ),
        rgbw=(0, 0, 0, 0),
    )
    color_events_contenor = color_events_check(
        valid_color_events,
    )
    assert not (color_events_contenor["Frame check"]["Values"].user_validation)


def test_invalid_color_events_rgbw_value_check(
    valid_color_events: ColorEvents,
):
    valid_color_events.add_timecode_rgbw(
        JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame + 2
        ),
        (JSON_BINARY_PARAMETER.chrome_value_bound.maximal + 1, 0, 0, 0),
    )
    color_events_contenor = color_events_check(
        valid_color_events,
    )
    assert not (color_events_contenor["Values"].user_validation)
