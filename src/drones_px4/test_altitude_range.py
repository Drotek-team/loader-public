from .drones_px4 import DroneUser, DronesPx4


def valid_drones_user(altitude_max: int) -> DronesPx4:
    drone_0 = DroneUser(0)
    drone_0.add_position(0, (0, 0, 0))
    drone_0.add_position(0, (0, 0, -altitude_max))
    drone_1 = DroneUser(1)
    drone_1.add_position(0, (0, 0, 0))
    drone_1.add_position(0, (0, 0, -altitude_max + 1))
    return DronesPx4([drone_0, drone_1])


def test_show_dutation():
    ALTITUDE_MAX = 1_532
    drones_user = valid_drones_user(ALTITUDE_MAX)
    assert drones_user.altitude_range == (-ALTITUDE_MAX, 0)
