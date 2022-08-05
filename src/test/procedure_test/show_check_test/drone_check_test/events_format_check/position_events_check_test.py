import os

import pytest

from ......drones_manager.drone.events.position_events import (
    PositionEvent,
    PositionEvents,
)
from ......parameter.parameter import Parameter
from ......procedure.show_check.drone_check.events_format_check.events_format_check_procedure import (
    position_events_check,
)
from ......procedure.show_check.drone_check.events_format_check.events_format_check_report import (
    PositionEventsCheckReport,
)


@pytest.fixture
def valid_position_events():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    takeoff_parameter = parameter.takeoff_parameter
    frame_parameter = parameter.frame_parameter
    position_events = PositionEvents()
    position_events.add(frame_parameter.show_duration_min_frame, (0, 0, 0))
    position_events.add(
        frame_parameter.show_duration_min_frame + takeoff_parameter.takeoff_duration,
        (0, 0, -takeoff_parameter.takeoff_altitude),
    )
    return position_events


@pytest.fixture
def position_events_check_report():
    return PositionEventsCheckReport()


def test_valid_position_events_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    position_events_check(
        valid_position_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert (
        position_events_check_report.takeoff_check_report.takeoff_position_check_report.validation
    )


def test_invalid_position_events_frame_format_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_position_events.add(
        1.23,
        (0, 0, 0),
    )
    position_events_check(
        valid_position_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.frame_check_report.frame_format_check_report.validation
    )


def test_invalid_position_events_frame_rate_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_position_events.add(
        parameter.frame_parameter.show_duration_min_frame + 1,
        (0, 0, 0),
    )
    position_events_check(
        valid_position_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.frame_check_report.frame_rate_check_report.validation
    )


def test_invalid_position_events_frame_increasing_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_position_events.add(
        parameter.frame_parameter.show_duration_min_frame,
        (0, 0, 0),
    )
    position_events_check(
        valid_position_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.frame_check_report.increasing_frame_check_report.validation
    )


def test_invalid_position_events_frame_first_frame_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_position_events.event_list.insert(
        0, PositionEvent(parameter.frame_parameter.show_duration_min_frame - 1, 0, 0, 0)
    )
    position_events_check(
        valid_position_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.frame_check_report.frame_value_check_report.validation
    )


def test_invalid_position_events_xyz_format_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_position_events.add(
        parameter.frame_parameter.show_duration_min_frame,
        (1.23, 0, 0),
    )
    position_events_check(
        valid_position_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.xyz_check_report.xyz_format_check_report.validation
    )


def test_invalid_position_events_xyz_value_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_position_events.add(
        parameter.frame_parameter.show_duration_min_frame,
        (parameter.iostar_parameter.position_value_max + 1, 0, 0),
    )
    position_events_check(
        valid_position_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.xyz_check_report.xyz_value_check_report.validation
    )


def test_invalid_position_events_takeoff_duration_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_position_events.event_list.insert(
        1, PositionEvent(parameter.frame_parameter.show_duration_min_frame + 1, 0, 0, 0)
    )
    position_events_check(
        valid_position_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.takeoff_check_report.takeoff_duration_check_report.validation
    )


# def test_invalid_position_events_takeoff_position_check(
#     valid_position_events: PositionEvents,
#     position_events_check_report: PositionEventsCheckReport,
# ):
#     parameter = Parameter()
#     parameter.load_export_parameter()
#     parameter.load_iostar_parameter()
#     valid_position_events.event_list.insert(
#         1, PositionEvent(parameter.frame_parameter.show_duration_min_frame, 0, 0, 0)
#     )
#     position_events_check(
#         valid_position_events,
#         parameter.frame_parameter,
#         parameter.iostar_parameter,
#         parameter.takeoff_parameter,
#         position_events_check_report,
#     )
#     assert not (
#         position_events_check_report.takeoff_check_report.takeoff_position_check_report.validation
#     )
