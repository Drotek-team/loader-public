from .show_px4 import DronePx4, ShowPx4


def valid_show_px4(show_duration: int) -> ShowPx4:

    drone_0 = DronePx4(0)
    drone_0.add_position(show_duration, (0, 0, 0))
    drone_1 = DronePx4(1)
    drone_1.add_position(show_duration - 1, (0, 0, 0))
    return ShowPx4([drone_0, drone_1])


def test_show_dutation():
    show_duration = 225_368
    show_px4 = valid_show_px4(show_duration)
    assert show_px4.duration == show_duration
