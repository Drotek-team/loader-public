import pytest

from ......drones_manager.drone.events.color_events import ColorEvent, ColorEvents
from ......parameter.parameter import Parameter
from ......procedure.show_check.drone_check.events_format_check.events_format_check_procedure import (
    color_events_check,
)
from ......procedure.show_check.drone_check.events_format_check.events_format_check_report import (
    ColorEventsCheckReport,
)


@pytest.fixture
def valid_color_events():
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    timecode_parameter = parameter.timecode_parameter
    color_events = ColorEvents()
    color_events.add(timecode_parameter.show_timecode_begin, (0, 0, 0, 0))
    color_events.add(
        timecode_parameter.show_timecode_begin + timecode_parameter.color_rate,
        (255, 255, 255, 255),
    )
    return color_events


@pytest.fixture
def color_events_check_report():
    return ColorEventsCheckReport()


def test_valid_color_events_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    color_events_check(
        valid_color_events,
        color_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert color_events_check_report.validation


def test_invalid_color_events_timecode_format_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_color_events.add(
        1.23,
        (0, 0, 0, 0),
    )
    color_events_check(
        valid_color_events,
        color_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        color_events_check_report.timecode_check_report.timecode_format_check_report.validation
    )


def test_invalid_color_events_timecode_rate_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_color_events.add(
        parameter.timecode_parameter.show_timecode_begin + 1,
        (0, 0, 0, 0),
    )
    color_events_check(
        valid_color_events,
        color_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        color_events_check_report.timecode_check_report.timecode_rate_check_report.validation
    )


def test_invalid_color_events_timecode_increasing_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_color_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        (0, 0, 0, 0),
    )
    color_events_check(
        valid_color_events,
        color_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        color_events_check_report.timecode_check_report.increasing_timecode_check_report.validation
    )


def test_invalid_color_events_timecode_first_timecode_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_color_events.event_list.insert(
        0, ColorEvent(parameter.timecode_parameter.show_timecode_begin - 1, 0, 0, 0, 0)
    )
    color_events_check(
        valid_color_events,
        color_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        color_events_check_report.timecode_check_report.first_timecode_check_report.validation
    )


def test_invalid_color_events_rgbw_format_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_color_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        (1.23, 0, 0, 0),
    )
    color_events_check(
        valid_color_events,
        color_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        color_events_check_report.rgbw_check_report.rgbw_format_check_report.validation
    )


def test_invalid_color_events_rgbw_value_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_export_parameter()
    parameter.load_iostar_parameter()
    valid_color_events.add(
        parameter.timecode_parameter.show_timecode_begin,
        (parameter.iostar_parameter.color_value_max + 1, 0, 0, 0),
    )
    color_events_check(
        valid_color_events,
        color_events_check_report,
        parameter.timecode_parameter,
        parameter.iostar_parameter,
    )
    assert not (
        color_events_check_report.rgbw_check_report.rgbw_value_check_report.validation
    )
