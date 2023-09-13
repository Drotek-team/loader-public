from typing import List

import pytest
from loader.reports import DanceSizeReport
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.drone_px4.events.magic_number import MagicNumber

MAGIC_BREAKER_NUMBER = 12497


@pytest.fixture
def valid_drone_dance_size() -> List[DronePx4]:
    autopilot_format = [DronePx4(i, MagicNumber.old) for i in range(2)]
    for drone in autopilot_format:
        for _ in range(MAGIC_BREAKER_NUMBER):
            drone.color_events.add_timecode_rgbw(0, (0, 0, 0, 0))
    return autopilot_format


@pytest.fixture
def invalid_drone_dance_size() -> List[DronePx4]:
    autopilot_format = [DronePx4(i, MagicNumber.old) for i in range(2)]
    for drone in autopilot_format:
        for _ in range(MAGIC_BREAKER_NUMBER + 1):
            drone.color_events.add_timecode_rgbw(0, (0, 0, 0, 0))
    return autopilot_format


def test_valid_drone_dance_size_report(valid_drone_dance_size: List[DronePx4]) -> None:
    dance_size_report = DanceSizeReport.generate(valid_drone_dance_size)
    assert len(dance_size_report) == len(dance_size_report.summarize()) == 0


def test_invalid_drone_dance_size_report(invalid_drone_dance_size: List[DronePx4]) -> None:
    dance_size_report = DanceSizeReport.generate(invalid_drone_dance_size)
    assert len(dance_size_report) == len(dance_size_report.summarize())
    assert (
        dance_size_report.summarize().model_dump()["dance_size_infractions_summary"][
            "drone_indices"
        ]
        == "0-1"
    )
