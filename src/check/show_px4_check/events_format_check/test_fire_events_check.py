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
            JSON_BINARY_PARAMETER.show_start_frame
        ),
        chanel=0,
        duration=0,
    )
    fire_events.add_timecode_chanel_duration(
        timecode=FRAME_PARAMETER.from_second_to_frame(
            JSON_BINARY_PARAMETER.show_start_frame
        )
        + 1,
        chanel=1,
        duration=0,
    )
    fire_events.add_timecode_chanel_duration(
        FRAME_PARAMETER.from_second_to_frame(JSON_BINARY_PARAMETER.show_start_frame)
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
            JSON_BINARY_PARAMETER.show_start_frame
        )
        - 1,
        chanel=0,
        duration=0,
    )
    fire_events_contenor = fire_events_check(
        valid_fire_events,
    )
    assert not (fire_events_contenor["Frame check"].user_validation)


def test_invalid_fire_events_chanel_value_check(
    valid_fire_events: FireEvents,
):
    valid_fire_events.add_timecode_chanel_duration(
        JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
        JSON_BINARY_PARAMETER.fire_chanel_value_bound.maximal + 1,
        0,
    )
    fire_events_contenor = fire_events_check(
        valid_fire_events,
    )
    assert not (fire_events_contenor["Fire chanel value check"].user_validation)


def test_invalid_fire_events_duration_value_check(
    valid_fire_events: FireEvents,
):
    valid_fire_events.add_timecode_chanel_duration(
        JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
        0,
        JSON_BINARY_PARAMETER.fire_duration_value_bound.maximal + 1,
    )
    fire_events_contenor = fire_events_check(
        valid_fire_events,
    )
    assert not (fire_events_contenor["Fire duration value check"].user_validation)
