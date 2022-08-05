from ...drones_manager.drones_manager import DroneExport, DronesManager
from ...parameter.parameter import Parameter
import os


def valid_drones_manager(show_duration: int) -> DronesManager:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    takeoff_parameter = parameter.takeoff_parameter
    drone_0 = DroneExport(0)
    drone_0.add_position(
        show_duration, (0, 0, -takeoff_parameter.takeoff_altitude_meter)
    )
    drone_1 = DroneExport(1)
    drone_1.add_position(
        show_duration - 1, (0, 0, -takeoff_parameter.takeoff_altitude_meter)
    )
    return DronesManager([drone_0, drone_1])


def test_show_dutation():
    SHOW_DURATION = 225_368
    drones_manager = valid_drones_manager(SHOW_DURATION)
    assert drones_manager.duration == SHOW_DURATION
