import pytest
from src.drones_manager.drone.events.position_events import PositionEvent

from ...drones_manager.drones_manager import Drone
from ...parameter.parameter import Parameter
from ...show_simulation.dance_simulation.convert_drone_to_dance_simulation import (
    flight_simulation,
    land_simulation,
    stand_by_simulation,
    takeoff_simulation,
)


@pytest.fixture
def valid_drone() -> Drone:
    valid_drone = Drone(0)
    valid_drone.add_position(0, (0, 0, 0))
    valid_drone.add_position(0, (0, 0, 1000))
    return valid_drone


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


# TO DO: find a god damn test setup
def test_land_simulation():
    parameter = Parameter()
    parameter.load_iostar_parameter()
    parameter.load_export_parameter()
    first_takeoff_position = (0, 0, 10_00)
    dance_sequence = land_simulation(
        first_takeoff_position,
        parameter.timecode_parameter,
        parameter.land_parameter,
        parameter.json_convention_constant,
    )
    assert all(dance_sequence.drone_in_air) == True
    assert all(dance_sequence.drone_in_dance) == False
