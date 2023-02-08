import pytest
from loader.check.show_px4_check.events_format_check.events_format_check import (
    position_events_check,
)
from loader.parameter.iostar_dance_import_parameter.frame_parameter import (
    FRAME_PARAMETER,
)
from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from loader.show_env.show_px4.drone_px4.events.position_events import PositionEvents


@pytest.fixture
def valid_position_events() -> PositionEvents:
    position_events = PositionEvents()
    position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETER.show_start_frame,
        (0, 0, 0),
    )
    position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame
            + FRAME_PARAMETER.from_second_to_frame(
                TAKEOFF_PARAMETER.takeoff_duration_second,
            ),
        ),
        (
            0,
            0,
            -int(TAKEOFF_PARAMETER.takeoff_altitude_meter_min),
        ),
    )
    return position_events


def test_valid_position_events_check(
    valid_position_events: PositionEvents,
) -> None:
    position_events_contenor = position_events_check(
        valid_position_events,
    )
    assert position_events_contenor.user_validation


def test_invalid_position_events_frame_increasing_check(
    valid_position_events: PositionEvents,
) -> None:
    position_events_contenor = position_events_check(valid_position_events)
    assert position_events_contenor["Frame check"]["Increasing"].user_validation
    valid_position_events.add_timecode_xyz(
        FRAME_PARAMETER.from_second_to_frame(JSON_BINARY_PARAMETER.show_start_frame),
        (0, 0, 0),
    )
    position_events_contenor = position_events_check(
        valid_position_events,
    )
    assert not (position_events_contenor["Frame check"]["Increasing"].user_validation)


def test_invalid_position_events_frame_first_frame_check(
    valid_position_events: PositionEvents,
) -> None:
    valid_position_events.add_timecode_xyz(
        timecode=JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame - 1,
        ),
        xyz=(0, 0, 0),
    )
    position_events_contenor = position_events_check(
        valid_position_events,
    )
    assert not (position_events_contenor["Frame check"]["Values"].user_validation)


def test_invalid_position_events_xyz_value_check(
    valid_position_events: PositionEvents,
) -> None:
    valid_position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
        (JSON_BINARY_PARAMETER.coordinate_value_bound.maximal + 1, 0, 0),
    )
    position_events_contenor = position_events_check(
        valid_position_events,
    )
    assert not (position_events_contenor.user_validation)
