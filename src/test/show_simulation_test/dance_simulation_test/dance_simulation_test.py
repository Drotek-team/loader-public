import numpy as np
import pytest
from src.drones_manager.drone.events.position_events import PositionEvent

from ....drones_manager.drones_manager import Drone
from ....parameter.parameter import Parameter
from ....show_simulation.dance_simulation.convert_drone_to_dance_simulation import (
    DanceSimulation,
    convert_drone_to_dance_simulation,
    flight_simulation,
    land_simulation,
    stand_by_simulation,
    takeoff_simulation,
)
from ....show_simulation.dance_simulation.position_simulation import (
    linear_interpolation,
)


@pytest.fixture
def valid_drone() -> Drone:
    parameter = Parameter()
    parameter.load_parameter()
    valid_drone = Drone(0)
    takeoff_timecode = 0
    transition_duration = 2_000
    transition_position = (200, 200)
    valid_drone.add_position(takeoff_timecode, (0, 0, 0))
    valid_drone.add_position(
        takeoff_timecode + parameter.takeoff_parameter.takeoff_duration,
        (0, 0, parameter.takeoff_parameter.takeoff_altitude),
    )
    valid_drone.add_position(
        takeoff_timecode
        + parameter.takeoff_parameter.takeoff_duration
        + transition_duration,
        (
            transition_position[0],
            transition_position[1],
            parameter.takeoff_parameter.takeoff_altitude,
        ),
    )
    return valid_drone


# def test_valid_drone(valid_drone: Drone):
#     parameter = Parameter()
#     parameter.load_parameter()
#     dance_sequence = convert_drone_to_dance_simulation(
#         valid_drone,
#         valid_drone.last_position_event.timecode,
#         parameter.timecode_parameter,
#         parameter.takeoff_parameter,
#         parameter.land_parameter,
#         parameter.json_convention_constant,
#     ).dance_sequence
#     popo = (
#         parameter.takeoff_parameter.takeoff_duration
#         // parameter.timecode_parameter.position_timecode_rate
#     )
#     assert list(dance_sequence.drone_positions[0]) == [0, 0, 0]
#     assert list(
#         dance_sequence.drone_positions[
#             parameter.takeoff_parameter.takeoff_duration
#             // parameter.timecode_parameter.position_timecode_rate
#         ]
#     ) == [
#         0,
#         0,
#         parameter.json_convention_constant.CENTIMETER_TO_METER_RATIO
#         * parameter.takeoff_parameter.takeoff_altitude,
#     ]
#     assert list(dance_sequence.drone_positions[-1]) == [
#         2,
#         2,
#         parameter.json_convention_constant.CENTIMETER_TO_METER_RATIO
#         * parameter.takeoff_parameter.takeoff_altitude,
#     ]
#     assert len(dance_sequence.drone_positions) == 0
