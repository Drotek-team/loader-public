import os

import pytest

from .....drones_px4.drone.drone import DroneUser
from .....parameter.parameter import Parameter
from .dances_size_check_procedure import (
    apply_dance_size_check_procedure,
)
from .dances_size_check_report import (
    DanceSizeCheckReport,
)

MAGIC_BREAKER_NUMBER = 16660


@pytest.fixture
def valid_drone_dance_size():
    drone = DroneUser(0)
    for _ in range(MAGIC_BREAKER_NUMBER):
        drone.color_events.add(0, (0, 0, 0, 0))
    return drone


@pytest.fixture
def invalid_drone_dance_size():
    drone = DroneUser(0)
    for _ in range(MAGIC_BREAKER_NUMBER + 1):
        drone.color_events.add(0, (0, 0, 0, 0))
    return drone


def test_valid_drone_dance_size_check(valid_drone_dance_size: DroneUser):
    dance_size_check_report = DanceSizeCheckReport()
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    apply_dance_size_check_procedure(
        valid_drone_dance_size,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        dance_size_check_report,
    )
    assert dance_size_check_report.validation


def test_invalid_drone_dance_size_check(invalid_drone_dance_size: DroneUser):
    dance_size_check_report = DanceSizeCheckReport()
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    apply_dance_size_check_procedure(
        invalid_drone_dance_size,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        dance_size_check_report,
    )
    assert not (dance_size_check_report.validation)
