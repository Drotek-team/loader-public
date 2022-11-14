import os

from ..parameter.parameter import Parameter
from .show_px4 import DronePx4, ShowPx4


def valid_show_px4(show_duration: int) -> ShowPx4:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    drone_0 = DronePx4(0)
    drone_0.add_position(show_duration, (0, 0, 0))
    drone_1 = DronePx4(1)
    drone_1.add_position(show_duration - 1, (0, 0, 0))
    return ShowPx4([drone_0, drone_1])


def test_show_dutation():
    SHOW_DURATION = 225_368
    show_px4 = valid_show_px4(SHOW_DURATION)
    assert show_px4.duration == SHOW_DURATION
