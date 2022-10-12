from .show_px4 import DronePx4, ShowPx4


def valid_show_px4(altitude_max: int) -> ShowPx4:
    drone_0 = DronePx4(0)
    drone_0.add_position(0, (0, 0, 0))
    drone_0.add_position(0, (0, 0, -altitude_max))
    drone_1 = DronePx4(1)
    drone_1.add_position(0, (0, 0, 0))
    drone_1.add_position(0, (0, 0, -altitude_max + 1))
    return ShowPx4([drone_0, drone_1])


def test_show_dutation():
    ALTITUDE_MAX = 1_532
    show_px4 = valid_show_px4(ALTITUDE_MAX)
    assert show_px4.altitude_range == (-ALTITUDE_MAX, 0)
