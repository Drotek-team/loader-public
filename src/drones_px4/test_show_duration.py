from .drones_px4 import DronePx4, DronesPx4
from ..parameter.parameter import Parameter
import os


def valid_drones_px4(show_duration: int) -> DronesPx4:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    drone_0 = DronePx4(0)
    drone_0.add_position(show_duration, (0, 0, 0))
    drone_1 = DronePx4(1)
    drone_1.add_position(show_duration - 1, (0, 0, 0))
    return DronesPx4([drone_0, drone_1])


def test_show_dutation():
    SHOW_DURATION = 225_368
    drones_px4 = valid_drones_px4(SHOW_DURATION)
    assert drones_px4.duration == SHOW_DURATION
