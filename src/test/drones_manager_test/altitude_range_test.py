from ...drones_manager.drones_manager import DroneExport, DronesManager
from ...parameter.parameter import Parameter
import os


def valid_drones_manager(altitude_max: int) -> DronesManager:
    drone_0 = DroneExport(0)
    drone_0.add_position(0, (0, 0, 0))
    drone_0.add_position(0, (0, 0, -altitude_max))
    drone_1 = DroneExport(1)
    drone_1.add_position(0, (0, 0, 0))
    drone_1.add_position(0, (0, 0, -altitude_max + 1))
    return DronesManager([drone_0, drone_1])


def test_show_dutation():
    ALTITUDE_MAX = 1_532
    drones_manager = valid_drones_manager(ALTITUDE_MAX)
    assert drones_manager.altitude_range == (-ALTITUDE_MAX, 0)
