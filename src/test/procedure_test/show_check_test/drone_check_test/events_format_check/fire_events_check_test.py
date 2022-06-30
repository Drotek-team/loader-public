import pytest

from ......drones_manager.drone.events.fire_events import FireEvent, FireEvents
from ......parameter.parameter import Parameter
from ......procedure.show_check.drone_check.events_format_check.events_format_check_procedure import (
    fire_events_check,
)
from ......procedure.show_check.drone_check.events_format_check.events_format_check_report import (
    FireEventsCheckReport,
)


@pytest.fixture
def valid_fire_events():
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    timecode_parameter = parameter.timecode_parameter
    fire_events = FireEvents()
    fire_events.add(timecode_parameter.show_timecode_begin, 0, 1000)
    fire_events.add(timecode_parameter.show_timecode_begin, 1, 1000)
    fire_events.add(timecode_parameter.show_timecode_begin, 2, 1000)
    return fire_events


@pytest.fixture
def fire_events_check_report():
    return FireEventsCheckReport()


def test_valid_fire_events_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    fire_events_check(
        valid_fire_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert (
        fire_events_check_report.fire_chanel_check_report.fire_chanel_format_check_report.validation
    )
    assert (
        fire_events_check_report.fire_chanel_check_report.fire_chanel_value_check_report.validation
    )
    assert (
        fire_events_check_report.fire_chanel_check_report.fire_chanel_unicty_check_report.validation
    )
    assert (
        fire_events_check_report.fire_duration_check_report.fire_duration_format_check_report.validation
    )
    assert (
        fire_events_check_report.fire_duration_check_report.fire_duration_value_check_report.validation
    )
    assert (
        fire_events_check_report.fire_timecode_check_report.timecode_value_check_report.validation
    )
    assert (
        fire_events_check_report.fire_timecode_check_report.timecode_format_check_report.validation
    )
    assert fire_events_check_report.validation


def test_invalid_fire_events_timecode_format_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.add(
        1.23,
        0,
        0,
    )
    fire_events_check(
        valid_fire_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert not (
        fire_events_check_report.fire_timecode_check_report.timecode_format_check_report.validation
    )


def test_invalid_fire_events_timecode_first_timecode_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.event_list.insert(
        0, FireEvent(parameter.timecode_parameter.show_timecode_begin - 1, 0, 0)
    )
    fire_events_check(
        valid_fire_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert not (
        fire_events_check_report.fire_timecode_check_report.timecode_value_check_report.validation
    )


def test_invalid_fire_events_chanel_format_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.add(parameter.timecode_parameter.show_timecode_begin, 1.23, 0)
    fire_events_check(
        valid_fire_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert not (
        fire_events_check_report.fire_chanel_check_report.fire_chanel_format_check_report.validation
    )


def test_invalid_fire_events_chanel_value_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        parameter.iostar_parameter.fire_chanel_value_max + 1,
        0,
    )
    fire_events_check(
        valid_fire_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert not (
        fire_events_check_report.fire_chanel_check_report.fire_chanel_value_check_report.validation
    )


def test_invalid_fire_events_chanel_unicity_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        parameter.iostar_parameter.fire_chanel_value_max,
        0,
    )
    valid_fire_events.add(
        parameter.timecode_parameter.show_timecode_begin + 1,
        parameter.iostar_parameter.fire_chanel_value_max,
        0,
    )
    fire_events_check(
        valid_fire_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert not (
        fire_events_check_report.fire_chanel_check_report.fire_chanel_unicty_check_report.validation
    )


def test_invalid_fire_events_duration_format_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.add(parameter.timecode_parameter.show_timecode_begin, 0, 1.23)
    fire_events_check(
        valid_fire_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert not (
        fire_events_check_report.fire_duration_check_report.fire_duration_format_check_report.validation
    )


def test_invalid_fire_events_duration_value_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        0,
        parameter.iostar_parameter.fire_duration_value_max + 1,
    )
    fire_events_check(
        valid_fire_events,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert not (
        fire_events_check_report.fire_duration_check_report.fire_duration_value_check_report.validation
    )
