from ..drones_px4.drones_px4 import DronePx4, DronesPx4


def valid_drones_px4(altitude_max: int) -> DronesPx4:
    drone_0 = DronePx4(0)
    drone_0.add_position(0, (0, 0, 0))
    drone_0.add_position(0, (0, 0, -altitude_max))
    drone_1 = DronePx4(1)
    drone_1.add_position(0, (0, 0, 0))
    drone_1.add_position(0, (0, 0, -altitude_max + 1))
    return DronesPx4([drone_0, drone_1])


def test_show_dutation():
    ALTITUDE_MAX = 1_532
    drones_px4 = valid_drones_px4(ALTITUDE_MAX)
    assert drones_px4.altitude_range == (-ALTITUDE_MAX, 0)
