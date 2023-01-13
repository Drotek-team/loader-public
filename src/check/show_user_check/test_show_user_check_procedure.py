import pytest

from ...migration.show_user.show_user import *
from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from .show_user_check_procedure import *
from .show_user_check_report import *


@pytest.fixture
def valid_drone_user() -> DroneUser:
    return DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min),
            ),
        ],
        color_events=[],
        fire_events=[],
    )


def test_valid_position_events_takeoff_duration_xyz_check(
    valid_drone_user: DroneUser,
):
    takeoff_check_report = TakeoffCheckReport()
    apply_takeoff_check(
        valid_drone_user,
        takeoff_check_report,
    )
    assert takeoff_check_report.validation


FRAME_BIAS = 1


@pytest.fixture
def invalid_drone_user_takeoff_duration() -> DroneUser:
    return DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                )
                + FRAME_BIAS,
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min),
            ),
        ],
        color_events=[],
        fire_events=[],
    )


def test_invalid_position_events_takeoff_duration_check(
    invalid_drone_user_takeoff_duration: DroneUser,
):
    takeoff_check_report = TakeoffCheckReport()
    apply_takeoff_check(
        invalid_drone_user_takeoff_duration,
        takeoff_check_report,
    )
    assert not (takeoff_check_report.takeoff_duration_check_report.validation)
    assert takeoff_check_report.takeoff_xyz_check_report.validation


Z_BIAS = 1e-2


@pytest.fixture
def invalid_drone_user_takeoff_xyz() -> DroneUser:
    return DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_max + Z_BIAS),
            ),
        ],
        color_events=[],
        fire_events=[],
    )


def test_invalid_position_events_takeoff_xyz_check(
    invalid_drone_user_takeoff_xyz: DroneUser,
):
    takeoff_check_report = TakeoffCheckReport()
    apply_takeoff_check(
        invalid_drone_user_takeoff_xyz,
        takeoff_check_report,
    )
    assert takeoff_check_report.takeoff_duration_check_report.validation
    assert not (takeoff_check_report.takeoff_xyz_check_report.validation)


def test_empty_position_events():
    empty_position_events_drone_user = DroneUser(
        position_events=[], color_events=[], fire_events=[]
    )
    takeoff_check_report = TakeoffCheckReport()
    apply_takeoff_check(
        empty_position_events_drone_user,
        takeoff_check_report,
    )
    assert not (takeoff_check_report.takeoff_duration_check_report.validation)
    assert not (takeoff_check_report.takeoff_xyz_check_report.validation)


def test_valid_one_position_events():
    one_position_events_drone_user = DroneUser(
        position_events=[PositionEventUser(frame=0, xyz=(2.0, 2.0, 0.0))],
        color_events=[],
        fire_events=[],
    )
    takeoff_check_report = TakeoffCheckReport()
    apply_takeoff_check(
        one_position_events_drone_user,
        takeoff_check_report,
    )
    assert takeoff_check_report.validation


def test_invalid_by_time_one_position_events():
    one_position_events_drone_user = DroneUser(
        position_events=[PositionEventUser(frame=1, xyz=(2.0, 2.0, 0.0))],
        color_events=[],
        fire_events=[],
    )
    takeoff_check_report = TakeoffCheckReport()
    apply_takeoff_check(
        one_position_events_drone_user,
        takeoff_check_report,
    )
    assert not (takeoff_check_report.takeoff_duration_check_report.validation)
    assert takeoff_check_report.takeoff_xyz_check_report.validation


def test_invalid_by_position_one_position_events():
    one_position_events_drone_user = DroneUser(
        position_events=[PositionEventUser(frame=0, xyz=[2.0, 2.0, 0.1])],
        color_events=[],
        fire_events=[],
    )
    takeoff_check_report = TakeoffCheckReport()
    apply_takeoff_check(
        one_position_events_drone_user,
        takeoff_check_report,
    )
    assert takeoff_check_report.takeoff_duration_check_report.validation
    assert not (takeoff_check_report.takeoff_xyz_check_report.validation)
