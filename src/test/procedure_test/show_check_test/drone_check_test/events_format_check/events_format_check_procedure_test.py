import pytest

from ......drones_manager.drone.events.position_events import PositionEvents
from ......parameter.parameter import Parameter
from ......procedure.show_check.drone_check.events_format_check.events_format_check_procedure import (
    position_events_check,
)
from ......procedure.show_check.drone_check.events_format_check.events_format_check_report import (
    PositionEventsCheckReport,
)


@pytest.fixture
def invalid_position_events_takeoff_check():
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    takeoff_parameter = parameter.takeoff_parameter
    timecode_parameter = parameter.timecode_parameter
    position_events = PositionEvents()
    position_events.add(timecode_parameter.show_time_begin, (0, 0, 0))
    position_events.add(
        timecode_parameter.show_time_begin + takeoff_parameter.takeoff_duration,
        (0, 0, takeoff_parameter.takeoff_altitude),
    )
    return position_events


@pytest.fixture
def invalid_position_events_timecode_format_check():
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    timecode_parameter = parameter.timecode_parameter
    position_events = PositionEvents()
    position_events.add(0, (0, 0, 0))
    position_events.add(timecode_parameter.position_frequence + 1, (0, 0, 0))
    return position_events


@pytest.fixture
def position_events_check_report():
    return PositionEventsCheckReport()


def test_invalid_position_events_timecode_format_check(
    invalid_position_events_timecode_check: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    position_events_check(
        invalid_position_events_timecode_check,
        position_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert not (position_events_check_report.timecode_check.validation)


def test_invalid_position_events_timecode_rate_check(
    invalid_position_events_timecode_check: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    position_events_check(
        invalid_position_events_timecode_check,
        position_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert not (position_events_check_report.timecode_check.validation)


def test_invalid_position_events_timecode_increasing_check(
    invalid_position_events_timecode_format_check: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    position_events_check(
        invalid_position_events_timecode_format_check,
        position_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert not (position_events_check_report.timecode_check.validation)


def test_invalid_position_events_timecode_first_timecode_check(
    invalid_position_events_timecode_check: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    position_events_check(
        invalid_position_events_timecode_check,
        position_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
    )
    assert not (position_events_check_report.timecode_check.validation)
