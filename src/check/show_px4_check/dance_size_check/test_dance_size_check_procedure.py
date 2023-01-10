import pytest

from ....report import Displayer
from ....show_px4.drone_px4.drone_px4 import DronePx4
from .dances_size_check_procedure import apply_dance_size_check_procedure

MAGIC_BREAKER_NUMBER = 16660


@pytest.fixture
def valid_drone_dance_size():
    drone = DronePx4(0)
    for _ in range(MAGIC_BREAKER_NUMBER):
        drone.color_events.add_frame_rgbw(0, (0, 0, 0, 0))
    return drone


@pytest.fixture
def invalid_drone_dance_size():
    drone = DronePx4(0)
    for _ in range(MAGIC_BREAKER_NUMBER + 1):
        drone.color_events.add_frame_rgbw(0, (0, 0, 0, 0))
    return drone


def test_valid_drone_dance_size_check(valid_drone_dance_size: DronePx4):
    dance_size_check_report = Displayer("Dance size check report")
    apply_dance_size_check_procedure(
        valid_drone_dance_size,
        dance_size_check_report,
    )
    assert dance_size_check_report.validation


def test_invalid_drone_dance_size_check(invalid_drone_dance_size: DronePx4):
    dance_size_check_report = Displayer("Dance size check report")
    apply_dance_size_check_procedure(
        invalid_drone_dance_size,
        dance_size_check_report,
    )
    assert not (dance_size_check_report.validation)
