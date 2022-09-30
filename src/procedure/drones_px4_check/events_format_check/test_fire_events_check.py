import os

import pytest

from ....drones_px4.drone_px4.events.fire_events import FireEvent, FireEvents
from ....parameter.parameter import Parameter
from .events_format_check_procedure import (
    fire_events_check,
)
from .events_format_check_report import (
    FireEventsCheckReport,
)


@pytest.fixture
def valid_fire_events():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    frame_parameter = parameter.frame_parameter
    fire_events = FireEvents()
    fire_events.add_frame_chanel_duration(
        frame_parameter.show_duration_min_frame, 0, 1000
    )
    fire_events.add_frame_chanel_duration(
        frame_parameter.show_duration_min_frame, 1, 1000
    )
    fire_events.add_frame_chanel_duration(
        frame_parameter.show_duration_min_frame, 2, 1000
    )
    return fire_events


@pytest.fixture
def fire_events_check_report():
    return FireEventsCheckReport()


def test_valid_fire_events_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    fire_events_check(
        valid_fire_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )

    assert fire_events_check_report.validation


def test_invalid_fire_events_frame_format_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_fire_events.add_frame_chanel_duration(
        1.23,
        0,
        0,
    )
    fire_events_check(
        valid_fire_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert not (
        fire_events_check_report.fire_frame_check_report.frame_format_check_report.validation
    )


def test_invalid_fire_events_frame_first_frame_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_fire_events.events.insert(
        0, FireEvent(parameter.frame_parameter.show_duration_min_frame - 1, 0, 0)
    )
    fire_events_check(
        valid_fire_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert not (
        fire_events_check_report.fire_frame_check_report.frame_value_check_report.validation
    )


def test_invalid_fire_events_chanel_format_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_fire_events.add_frame_chanel_duration(
        parameter.frame_parameter.show_duration_min_frame, 1.23, 0
    )
    fire_events_check(
        valid_fire_events,
        parameter.frame_parameter,
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
    parameter.load_parameter(os.getcwd())
    valid_fire_events.add_frame_chanel_duration(
        parameter.frame_parameter.show_duration_min_frame,
        parameter.iostar_parameter.fire_chanel_value_max + 1,
        0,
    )
    fire_events_check(
        valid_fire_events,
        parameter.frame_parameter,
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
    parameter.load_parameter(os.getcwd())
    valid_fire_events.add_frame_chanel_duration(
        parameter.frame_parameter.show_duration_min_frame,
        parameter.iostar_parameter.fire_chanel_value_max,
        0,
    )
    valid_fire_events.add_frame_chanel_duration(
        parameter.frame_parameter.show_duration_min_frame + 1,
        parameter.iostar_parameter.fire_chanel_value_max,
        0,
    )
    fire_events_check(
        valid_fire_events,
        parameter.frame_parameter,
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
    parameter.load_parameter(os.getcwd())
    valid_fire_events.add_frame_chanel_duration(
        parameter.frame_parameter.show_duration_min_frame, 0, 1.23
    )
    fire_events_check(
        valid_fire_events,
        parameter.frame_parameter,
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
    parameter.load_parameter(os.getcwd())
    valid_fire_events.add_frame_chanel_duration(
        parameter.frame_parameter.show_duration_min_frame,
        0,
        parameter.iostar_parameter.fire_duration_value_frame_max + 1,
    )
    fire_events_check(
        valid_fire_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert not (
        fire_events_check_report.fire_duration_check_report.fire_duration_value_check_report.validation
    )


def test_invalid_fire_events_simulteanous_value_check(
    valid_fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_fire_events.add_frame_chanel_duration(
        parameter.frame_parameter.show_duration_min_frame,
        0,
        parameter.iostar_parameter.fire_duration_value_frame_max,
    )
    valid_fire_events.add_frame_chanel_duration(
        parameter.frame_parameter.show_duration_min_frame,
        0,
        parameter.iostar_parameter.fire_duration_value_frame_max,
    )
    fire_events_check(
        valid_fire_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        fire_events_check_report,
    )
    assert not (
        fire_events_check_report.fire_frame_check_report.increasing_frame_check_report.validation
    )
