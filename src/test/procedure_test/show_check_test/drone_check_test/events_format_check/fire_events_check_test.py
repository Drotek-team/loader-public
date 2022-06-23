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
        fire_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert (
        fire_events_check_report.fire_duration_check_report.fire_duration_format_check_report.validation
    )
    assert (
        fire_events_check_report.fire_duration_check_report.fire_duration_value_check_report.validation
    )
    assert fire_events_check_report.fire_duration_check_report.validation
    assert fire_events_check_report.fire_chanel_check_report.validation


def test_invalid_fire_events_timecode_format_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.add(
        1.23,
        (0, 0, 0, 0),
    )
    fire_events_check(
        valid_fire_events,
        fire_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        fire_events_check_report.timecode_check_report.timecode_format_check_report.validation
    )


def test_invalid_fire_events_timecode_rate_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.add(
        parameter.timecode_parameter.show_timecode_begin + 1,
        (0, 0, 0, 0),
    )
    fire_events_check(
        valid_fire_events,
        fire_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        fire_events_check_report.timecode_check_report.timecode_rate_check_report.validation
    )


def test_invalid_fire_events_timecode_increasing_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        (0, 0, 0, 0),
    )
    fire_events_check(
        valid_fire_events,
        fire_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        fire_events_check_report.timecode_check_report.increasing_timecode_check_report.validation
    )


def test_invalid_fire_events_timecode_first_timecode_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.event_list.insert(
        0, FireEvent(parameter.timecode_parameter.show_timecode_begin - 1, 0, 0, 0, 0)
    )
    fire_events_check(
        valid_fire_events,
        fire_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        fire_events_check_report.timecode_check_report.first_timecode_check_report.validation
    )


def test_invalid_fire_events_rgbw_format_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        (1.23, 0, 0, 0),
    )
    fire_events_check(
        valid_fire_events,
        fire_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        fire_events_check_report.rgbw_check_report.rgbw_format_check_report.validation
    )


def test_invalid_fire_events_rgbw_value_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_fire_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        (parameter.iostar_parameter.fire_format_max, 0, 0, 0),
    )
    fire_events_check(
        valid_fire_events,
        fire_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        fire_events_check_report.rgbw_check_report.rgbw_value_check_report.validation
    )
