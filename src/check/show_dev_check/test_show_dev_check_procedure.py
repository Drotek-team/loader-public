import os

import pytest

from ...parameter.parameter import Parameter
from ...show_dev.show_dev import DroneDev, PositionEventDev
from .show_dev_check_procedure import takeoff_check
from .show_dev_check_report import TakeoffCheckReport


@pytest.fixture
def valid_drone_dev() -> DroneDev:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    return DroneDev(
        0,
        [
            PositionEventDev(0, (0.0, 0.0, 0.0)),
            PositionEventDev(
                int(
                    parameter.frame_parameter.json_fps
                    * parameter.takeoff_parameter.takeoff_duration_second
                ),
                (0.0, 0.0, parameter.takeoff_parameter.takeoff_altitude_meter),
            ),
        ],
    )


def test_valid_position_events_takeoff_duration_xyz_check(
    valid_drone_dev: DroneDev,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    takeoff_check_report = TakeoffCheckReport()
    takeoff_check(
        valid_drone_dev,
        takeoff_check_report,
        parameter.takeoff_parameter,
        parameter.frame_parameter,
    )
    assert takeoff_check_report.validation


@pytest.fixture
def invalid_drone_dev_takeoff_duration() -> DroneDev:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    FRAME_BIAS = 1
    return DroneDev(
        0,
        [
            PositionEventDev(0, (0.0, 0.0, 0.0)),
            PositionEventDev(
                int(
                    parameter.frame_parameter.json_fps
                    * parameter.takeoff_parameter.takeoff_duration_second
                )
                + FRAME_BIAS,
                (0.0, 0.0, parameter.takeoff_parameter.takeoff_altitude_meter),
            ),
        ],
    )


def test_invalid_position_events_takeoff_duration_check(
    invalid_drone_dev_takeoff_duration: DroneDev,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    takeoff_check_report = TakeoffCheckReport()
    takeoff_check(
        invalid_drone_dev_takeoff_duration,
        takeoff_check_report,
        parameter.takeoff_parameter,
        parameter.frame_parameter,
    )
    assert not (takeoff_check_report.takeoff_duration_check_report.validation)
    assert takeoff_check_report.takeoff_xyz_check_report.validation


@pytest.fixture
def invalid_drone_dev_takeoff_xyz() -> DroneDev:
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    Z_BIAS = 1e-2
    return DroneDev(
        0,
        [
            PositionEventDev(0, (0.0, 0.0, 0.0)),
            PositionEventDev(
                int(
                    parameter.frame_parameter.json_fps
                    * parameter.takeoff_parameter.takeoff_duration_second
                ),
                (0.0, 0.0, parameter.takeoff_parameter.takeoff_altitude_meter + Z_BIAS),
            ),
        ],
    )


def test_invalid_position_events_takeoff_xyz_check(
    invalid_drone_dev_takeoff_xyz: DroneDev,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    takeoff_check_report = TakeoffCheckReport()
    takeoff_check(
        invalid_drone_dev_takeoff_xyz,
        takeoff_check_report,
        parameter.takeoff_parameter,
        parameter.frame_parameter,
    )
    assert takeoff_check_report.takeoff_duration_check_report.validation
    assert not (takeoff_check_report.takeoff_xyz_check_report.validation)
