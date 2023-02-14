import pytest
from loader.check.show_px4_check.dance_size_check.dances_size_check import (
    get_dance_size_infraction,
)
from loader.report import get_base_report_validation
from loader.show_env.show_px4.drone_px4.drone_px4 import DronePx4

MAGIC_BREAKER_NUMBER = 12495


@pytest.fixture
def valid_drone_dance_size() -> DronePx4:
    drone = DronePx4(0)
    for _ in range(MAGIC_BREAKER_NUMBER):
        drone.color_events.add_timecode_rgbw(0, (0, 0, 0, 0))
    return drone


@pytest.fixture
def invalid_drone_dance_size() -> DronePx4:
    drone = DronePx4(0)
    for _ in range(MAGIC_BREAKER_NUMBER + 1):
        drone.color_events.add_timecode_rgbw(0, (0, 0, 0, 0))
    return drone


def test_valid_drone_dance_size_check(valid_drone_dance_size: DronePx4) -> None:
    dance_size_check_report = get_dance_size_infraction(
        valid_drone_dance_size,
    )
    assert get_base_report_validation(dance_size_check_report)


def test_invalid_drone_dance_size_check(invalid_drone_dance_size: DronePx4) -> None:
    dance_size_check_report = get_dance_size_infraction(
        invalid_drone_dance_size,
    )
    assert not (get_base_report_validation(dance_size_check_report))
