import numpy as np
import pytest
from src.drones_manager.drone.events.position_events import PositionEvent

from ...drones_manager.drones_manager import Drone
from ...parameter.parameter import Parameter
from ...show_simulation.dance_simulation.convert_drone_to_dance_simulation import (
    DanceSimulation,
    convert_drone_to_dance_simulation,
    flight_simulation,
    land_simulation,
    stand_by_simulation,
    takeoff_simulation,
)
from ...show_simulation.dance_simulation.position_simulation import linear_interpolation


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


def test_stand_by_simulation():
    parameter = Parameter()
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    timecode_start = 0
    timecode_end = 1000
    first_takeoff_position = (0, 0, 10_00)
    dance_sequence = stand_by_simulation(
        timecode_start,
        timecode_end,
        first_takeoff_position,
        parameter.timecode_parameter,
        parameter.json_convention_constant,
    )
    assert len(dance_sequence.drone_positions) == 4
    assert all(dance_sequence.drone_in_air) == False
    assert all(dance_sequence.drone_in_dance) == False


# TO DO: find a god damn test setup
def test_takeoff_simulation():
    parameter = Parameter()
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    first_position = (0.0, 0.0, 0.0)
    dance_sequence = takeoff_simulation(
        first_position,
        parameter.timecode_parameter,
        parameter.takeoff_parameter,
        parameter.json_convention_constant,
    )
    assert dance_sequence.drone_positions[0][0] == first_position[0]
    assert all(dance_sequence.drone_in_air) == True
    assert all(dance_sequence.drone_in_dance) == False


# TO DO: find a god damn test setup
def test_flight_simulation():
    parameter = Parameter()
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    position_events = [
        PositionEvent(0, 0, 0, 0),
        PositionEvent(250, 0, 0, 100),
        PositionEvent(500, 0, 0, 200),
    ]
    dance_sequence = flight_simulation(
        position_events,
        parameter.timecode_parameter,
        parameter.json_convention_constant,
    )
    assert all(dance_sequence.drone_in_air) == True
    assert all(dance_sequence.drone_in_dance) == True


def test_land_simulation_first_case():
    parameter = Parameter()
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    X_CENTIMETER = 2_00
    Y_CENTIMETER = 2_00
    HGT_CENTIMETER = 1_00
    first_takeoff_position = (X_CENTIMETER, Y_CENTIMETER, HGT_CENTIMETER)
    dance_sequence = land_simulation(
        first_takeoff_position,
        parameter.timecode_parameter,
        parameter.land_parameter,
        parameter.json_convention_constant,
    )
    THEORICAL_LAST_TAKEOFF_POSITION = (X_CENTIMETER, Y_CENTIMETER, 0)
    THEORICAL_NB_POINT = (
        parameter.land_parameter.get_first_land_timecode_delta(HGT_CENTIMETER)
        // parameter.timecode_parameter.position_timecode_rate
    )
    theorical_curve = linear_interpolation(
        first_takeoff_position,
        THEORICAL_LAST_TAKEOFF_POSITION,
        THEORICAL_NB_POINT,
        parameter.json_convention_constant,
    )
    assert all(
        [
            all(drone_position == theorical_position)
            for drone_position, theorical_position in zip(
                dance_sequence.drone_positions, theorical_curve
            )
        ]
    )
    assert all(dance_sequence.drone_in_air) == True
    assert all(dance_sequence.drone_in_dance) == False


def test_land_simulation_second_case():
    parameter = Parameter()
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    X_CENTIMETER = 2_00
    Y_CENTIMETER = 2_00
    HGT_CENTIMETER = 5_00
    first_takeoff_position = (X_CENTIMETER, Y_CENTIMETER, HGT_CENTIMETER)
    dance_sequence = land_simulation(
        first_takeoff_position,
        parameter.timecode_parameter,
        parameter.land_parameter,
        parameter.json_convention_constant,
    )
    THEORICAL_MIDDLE_TAKEOFF_POSITION = (
        X_CENTIMETER,
        Y_CENTIMETER,
        parameter.land_parameter.land_safe_hgt,
    )
    THEORICAL_END_TAKEOFF_POSITION = (
        X_CENTIMETER,
        Y_CENTIMETER,
        0,
    )
    FIRST_THEORICAL_NB_POINT = (
        parameter.land_parameter.get_first_land_timecode_delta(HGT_CENTIMETER)
        // parameter.timecode_parameter.position_timecode_rate
    )
    first_theorical_curve = linear_interpolation(
        first_takeoff_position,
        THEORICAL_MIDDLE_TAKEOFF_POSITION,
        FIRST_THEORICAL_NB_POINT,
        parameter.json_convention_constant,
    )
    SECOND_THEORICAL_NB_POINT = (
        parameter.land_parameter.get_second_land_timecode_delta(HGT_CENTIMETER)
        // parameter.timecode_parameter.position_timecode_rate
    )
    second_theorical_curve = linear_interpolation(
        THEORICAL_MIDDLE_TAKEOFF_POSITION,
        THEORICAL_END_TAKEOFF_POSITION,
        SECOND_THEORICAL_NB_POINT,
        parameter.json_convention_constant,
    )
    theorical_curve = first_theorical_curve + second_theorical_curve
    assert len(dance_sequence.drone_positions) == len(theorical_curve)
    assert all(
        [
            np.array_equal(drone_position, theorical_position)
            for drone_position, theorical_position in zip(
                dance_sequence.drone_positions,
                theorical_curve,
            )
        ]
    )
    assert all(dance_sequence.drone_in_air) == True
    assert all(dance_sequence.drone_in_dance) == False
