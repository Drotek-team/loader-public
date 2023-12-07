from typing import List

import pytest
from loader.parameters.json_binary_parameters import LandType, MagicNumber
from loader.reports import DanceSizeReport
from loader.schemas.drone_px4 import DronePx4

MAGIC_BREAKER_NUMBER = 12497
NEW_MAGIC_BREAKER_NUMBER = 16663


@pytest.fixture
def valid_drone_dance_size(request: pytest.FixtureRequest) -> List[DronePx4]:
    autopilot_format = [DronePx4(i, request.param, 1, LandType.Land) for i in range(2)]
    magic_number_breaker = (
        MAGIC_BREAKER_NUMBER if request.param == MagicNumber.v1 else NEW_MAGIC_BREAKER_NUMBER
    )
    for drone in autopilot_format:
        for _ in range(magic_number_breaker):
            drone.color_events.add_timecode_rgbw(0, (0, 0, 0, 0))
    return autopilot_format


@pytest.fixture
def invalid_drone_dance_size(request: pytest.FixtureRequest) -> List[DronePx4]:
    autopilot_format = [DronePx4(i, request.param, 1, LandType.Land) for i in range(2)]
    magic_number_breaker = (
        MAGIC_BREAKER_NUMBER if request.param == MagicNumber.v1 else NEW_MAGIC_BREAKER_NUMBER
    )
    for drone in autopilot_format:
        for _ in range(magic_number_breaker + 1):
            drone.color_events.add_timecode_rgbw(0, (0, 0, 0, 0))
    return autopilot_format


@pytest.mark.parametrize("valid_drone_dance_size", list(MagicNumber), indirect=True)
def test_valid_drone_dance_size_report(valid_drone_dance_size: List[DronePx4]) -> None:
    dance_size_report = DanceSizeReport.generate(valid_drone_dance_size)
    assert len(dance_size_report) == len(dance_size_report.summarize()) == 0


@pytest.mark.parametrize("invalid_drone_dance_size", list(MagicNumber), indirect=True)
def test_invalid_drone_dance_size_report(invalid_drone_dance_size: List[DronePx4]) -> None:
    dance_size_report = DanceSizeReport.generate(invalid_drone_dance_size)
    assert len(dance_size_report) == len(dance_size_report.summarize())
    assert (
        dance_size_report.summarize().model_dump()["dance_size_infractions_summary"][
            "drone_indices"
        ]
        == "0-1"
    )
