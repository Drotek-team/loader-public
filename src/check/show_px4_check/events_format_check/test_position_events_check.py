import pytest

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ....parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ....show_env.show_px4.drone_px4.events.position_events import PositionEvents
from .events_format_check_procedure import position_events_check


@pytest.fixture
def valid_position_events():
    position_events = PositionEvents()
    position_events.add_timecode_xyz(
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        ),
        (0, 0, 0),
    )
    position_events.add_timecode_xyz(
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        )
        + int(TAKEOFF_PARAMETER.takeoff_duration_second * FRAME_PARAMETER.absolute_fps),
        (
            0,
            0,
            -int(TAKEOFF_PARAMETER.takeoff_altitude_meter_min),
        ),
    )
    return position_events


def test_valid_position_events_check(
    valid_position_events: PositionEvents,
):
    position_events_contenor = position_events_check(
        valid_position_events,
    )
    assert position_events_contenor.user_validation


def test_invalid_position_events_frame_increasing_check(
    valid_position_events: PositionEvents,
):
    position_events_contenor = position_events_check(valid_position_events)
    assert position_events_contenor["Frame check"]["Increasing"].user_validation
    valid_position_events.add_timecode_xyz(
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        ),
        (0, 0, 0),
    )
    position_events_contenor = position_events_check(
        valid_position_events,
    )
    assert not (position_events_contenor["Frame check"]["Increasing"].user_validation)


def test_invalid_position_events_frame_first_frame_check(
    valid_position_events: PositionEvents,
):
    valid_position_events.add_timecode_xyz(
        timecode=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_min_second
        )
        - 1,
        xyz=(0, 0, 0),
    )
    position_events_contenor = position_events_check(
        valid_position_events,
    )
    assert not (position_events_contenor["Frame check"]["Value"].user_validation)


def test_invalid_position_events_xyz_value_check(
    valid_position_events: PositionEvents,
):
    valid_position_events.add_timecode_xyz(
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            JSON_BINARY_PARAMETER.show_duration_max_second
        ),
        (JSON_BINARY_PARAMETER.position_value_max + 1, 0, 0),
    )
    position_events_contenor = position_events_check(
        valid_position_events,
    )
    assert not (position_events_contenor.user_validation)
