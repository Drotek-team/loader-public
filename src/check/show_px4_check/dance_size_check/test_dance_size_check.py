import pytest

from src.show_env.show_px4.drone_px4.drone_px4 import DronePx4

from .dances_size_check import apply_dance_size_check

MAGIC_BREAKER_NUMBER = 12495


@pytest.fixture
def valid_drone_dance_size():
    drone = DronePx4(0)
    for _ in range(MAGIC_BREAKER_NUMBER):
        drone.color_events.add_timecode_rgbw(0, (0, 0, 0, 0))
    return drone


@pytest.fixture
def invalid_drone_dance_size():
    drone = DronePx4(0)
    for _ in range(MAGIC_BREAKER_NUMBER + 1):
        drone.color_events.add_timecode_rgbw(0, (0, 0, 0, 0))
    return drone


def test_valid_drone_dance_size_check(valid_drone_dance_size: DronePx4):
    dance_size_check_report = apply_dance_size_check(
        valid_drone_dance_size,
    )
    assert dance_size_check_report.user_validation


def test_invalid_drone_dance_size_check(invalid_drone_dance_size: DronePx4):
    dance_size_check_report = apply_dance_size_check(
        invalid_drone_dance_size,
    )
    assert not (dance_size_check_report.user_validation)