import pytest
from loader.report.autopilot_format_report.dances_size_report import DanceSizeInfraction
from loader.report.base import get_report_validation
from loader.show_env.autopilot_format.drone_px4 import DronePx4

MAGIC_BREAKER_NUMBER = 12497


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


def test_valid_drone_dance_size_report(valid_drone_dance_size: DronePx4) -> None:
    dance_size_report = DanceSizeInfraction.generate(
        valid_drone_dance_size,
    )
    assert get_report_validation(dance_size_report)


def test_invalid_drone_dance_size_report(invalid_drone_dance_size: DronePx4) -> None:
    dance_size_report = DanceSizeInfraction.generate(
        invalid_drone_dance_size,
    )
    assert not get_report_validation(dance_size_report)
