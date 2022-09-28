from .drones_user import DroneUser, DronesUser
from ..parameter.parameter import Parameter
import os


def valid_drones_user(show_duration: int) -> DronesUser:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    takeoff_parameter = parameter.takeoff_parameter
    drone_0 = DroneUser(0)
    drone_0.add_position(
        show_duration, (0, 0, -takeoff_parameter.takeoff_altitude_meter)
    )
    drone_1 = DroneUser(1)
    drone_1.add_position(
        show_duration - 1, (0, 0, -takeoff_parameter.takeoff_altitude_meter)
    )
    return DronesUser([drone_0, drone_1])


def test_show_dutation():
    SHOW_DURATION = 225_368
    drones_user = valid_drones_user(SHOW_DURATION)
    assert drones_user.duration == SHOW_DURATION
