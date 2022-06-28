import pytest

from ...drones_manager.drones_manager import Drone
from ...parameter.parameter import Parameter
from ...show_simulation.dance_simulation.dance_simulation import (
    convert_drone_to_dance_simulation,
)


@pytest.fixture
def valid_drone() -> Drone:
    valid_drone = Drone()
    valid_drone.add_position(0, (0, 0, 0))
    valid_drone.add_position(0, (0, 0, 1000))
    return valid_drone


def test_show_simulation_convertion(valid_drone: Drone):
    parameter = Parameter()
    parameter.load_export_parameter()
    SHOW_END_TIMECODE = 30_000
    dance_simulation = convert_drone_to_dance_simulation(
        valid_drone, SHOW_END_TIMECODE, parameter.timecode_parameter
    )
    assert dance_simulation.drone_positions == 0
