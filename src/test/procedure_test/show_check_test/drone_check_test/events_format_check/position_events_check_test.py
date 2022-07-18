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
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    takeoff_parameter = parameter.takeoff_parameter
    timecode_parameter = parameter.timecode_parameter
    position_events = PositionEvents()
    position_events.add(timecode_parameter.show_timecode_begin, (0, 0, 0))
    position_events.add(
        timecode_parameter.show_timecode_begin + takeoff_parameter.takeoff_duration,
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
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    position_events_check(
        valid_position_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert (
        position_events_check_report.takeoff_check_report.takeoff_position_check_report.validation
    )


def test_invalid_position_events_timecode_format_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_position_events.add(
        1.23,
        (0, 0, 0),
    )
    position_events_check(
        valid_position_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.timecode_check_report.timecode_format_check_report.validation
    )


def test_invalid_position_events_timecode_rate_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_position_events.add(
        parameter.timecode_parameter.show_timecode_begin + 1,
        (0, 0, 0),
    )
    position_events_check(
        valid_position_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.timecode_check_report.timecode_rate_check_report.validation
    )


def test_invalid_position_events_timecode_increasing_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_position_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        (0, 0, 0),
    )
    position_events_check(
        valid_position_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.timecode_check_report.increasing_timecode_check_report.validation
    )


def test_invalid_position_events_timecode_first_timecode_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_position_events.event_list.insert(
        0, PositionEvent(parameter.timecode_parameter.show_timecode_begin - 1, 0, 0, 0)
    )
    position_events_check(
        valid_position_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.timecode_check_report.timecode_value_check_report.validation
    )


def test_invalid_position_events_xyz_format_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_position_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        (1.23, 0, 0),
    )
    position_events_check(
        valid_position_events,
        parameter.timecode_parameter,
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
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_position_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        (parameter.iostar_parameter.position_value_max + 1, 0, 0),
    )
    position_events_check(
        valid_position_events,
        parameter.timecode_parameter,
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
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_position_events.event_list.insert(
        1, PositionEvent(parameter.timecode_parameter.show_timecode_begin + 1, 0, 0, 0)
    )
    position_events_check(
        valid_position_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.takeoff_check_report.takeoff_duration_check_report.validation
    )


def test_invalid_position_events_takeoff_position_check(
    valid_position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_position_events.event_list.insert(
        1, PositionEvent(parameter.timecode_parameter.show_timecode_begin, 0, 0, 0)
    )
    position_events_check(
        valid_position_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        position_events_check_report,
    )
    assert not (
        position_events_check_report.takeoff_check_report.takeoff_position_check_report.validation
    )
