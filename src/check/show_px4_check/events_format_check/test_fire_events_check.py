import pytest

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ....show_env.show_px4.drone_px4.events.fire_events import FireEvents
from .events_format_check_procedure import fire_events_check


@pytest.fixture
def valid_fire_events():
    fire_events = FireEvents()
    fire_events.add_timecode_chanel_duration(
        timecode=FRAME_PARAMETER.from_second_to_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        ),
        chanel=0,
        duration=0,
    )
    fire_events.add_timecode_chanel_duration(
        timecode=FRAME_PARAMETER.from_second_to_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        )
        + 1,
        chanel=1,
        duration=0,
    )
    fire_events.add_timecode_chanel_duration(
        FRAME_PARAMETER.from_second_to_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        )
        + 2,
        chanel=2,
        duration=0,
    )
    return fire_events


def test_valid_fire_events_check(
    valid_fire_events: FireEvents,
):
    fire_events_contenor = fire_events_check(
        valid_fire_events,
    )
    assert fire_events_contenor.user_validation


def test_invalid_fire_events_frame_first_frame_check(
    valid_fire_events: FireEvents,
):
    valid_fire_events.add_timecode_chanel_duration(
        timecode=FRAME_PARAMETER.from_second_to_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        )
        - 1,
        chanel=0,
        duration=0,
    )
    fire_events_contenor = fire_events_check(
        valid_fire_events,
    )
    assert not (fire_events_contenor["Frame check"]["Value"].user_validation)


def test_invalid_fire_events_chanel_value_check(
    valid_fire_events: FireEvents,
):
    valid_fire_events.add_timecode_chanel_duration(
        FRAME_PARAMETER.from_second_to_frame(
            JSON_BINARY_PARAMETER.show_duration_max_second
        ),
        JSON_BINARY_PARAMETER.fire_chanel_value_max + 1,
        0,
    )
    fire_events_contenor = fire_events_check(
        valid_fire_events,
    )
    assert not (fire_events_contenor["Fire chanel check"]["Value"].user_validation)


def test_invalid_fire_events_duration_value_check(
    valid_fire_events: FireEvents,
):
    valid_fire_events.add_timecode_chanel_duration(
        FRAME_PARAMETER.from_second_to_frame(
            JSON_BINARY_PARAMETER.show_duration_max_second
        ),
        0,
        JSON_BINARY_PARAMETER.fire_duration_value_frame_max + 1,
    )
    fire_events_contenor = fire_events_check(
        valid_fire_events,
    )
    assert not (fire_events_contenor["Fire duration check"]["Value"].user_validation)
