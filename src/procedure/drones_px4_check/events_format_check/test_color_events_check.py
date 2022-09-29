import os

import pytest

from ....drones_px4.drone_px4.events.color_events import ColorEvent, ColorEvents
from ....parameter.parameter import Parameter
from .events_format_check_procedure import (
    color_events_check,
)
from .events_format_check_report import (
    ColorEventsCheckReport,
)


@pytest.fixture
def valid_color_events():
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    frame_parameter = parameter.frame_parameter
    color_events = ColorEvents()
    color_events.add(frame_parameter.show_duration_min_frame, (0, 0, 0, 0))
    color_events.add(
        frame_parameter.show_duration_min_frame + 1,
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
    parameter.load_parameter(os.getcwd())
    color_events_check(
        valid_color_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        color_events_check_report,
    )
    assert (
        color_events_check_report.frame_check_report.frame_rate_check_report.validation
    )


def test_invalid_color_events_frame_format_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_color_events.add(
        1.23,
        (0, 0, 0, 0),
    )
    color_events_check(
        valid_color_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        color_events_check_report,
    )
    assert not (
        color_events_check_report.frame_check_report.frame_format_check_report.validation
    )


# def test_invalid_color_events_frame_rate_check(
#     valid_color_events: ColorEvents,
#     color_events_check_report: ColorEventsCheckReport,
# ):
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     valid_color_events.add(
#         valid_color_events.event_list[-1].frame + 1,
#         (0, 0, 0, 0),
#     )
#     color_events_check(
#         valid_color_events,
#         parameter.frame_parameter,
#         parameter.iostar_parameter,
#         color_events_check_report,
#     )
#     assert not (
#         color_events_check_report.frame_check_report.frame_rate_check_report.validation
#     )


def test_invalid_color_events_frame_increasing_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_color_events.add(
        parameter.frame_parameter.show_duration_min_frame,
        (0, 0, 0, 0),
    )
    color_events_check(
        valid_color_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        color_events_check_report,
    )
    assert not (
        color_events_check_report.frame_check_report.increasing_frame_check_report.validation
    )


def test_invalid_color_events_frame_first_frame_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_color_events.event_list.insert(
        0, ColorEvent(parameter.frame_parameter.show_duration_min_frame - 1, 0, 0, 0, 0)
    )
    color_events_check(
        valid_color_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        color_events_check_report,
    )
    assert not (
        color_events_check_report.frame_check_report.frame_value_check_report.validation
    )


def test_invalid_color_events_rgbw_format_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_color_events.add(
        parameter.frame_parameter.show_duration_min_frame,
        (1.23, 0, 0, 0),
    )
    color_events_check(
        valid_color_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        color_events_check_report,
    )
    assert not (
        color_events_check_report.rgbw_check_report.rgbw_format_check_report.validation
    )


def test_invalid_color_events_rgbw_value_check(
    valid_color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    parameter = Parameter()
    parameter.load_parameter(os.getcwd())
    valid_color_events.add(
        parameter.frame_parameter.show_duration_min_frame,
        (parameter.iostar_parameter.color_value_max + 1, 0, 0, 0),
    )
    color_events_check(
        valid_color_events,
        parameter.frame_parameter,
        parameter.iostar_parameter,
        color_events_check_report,
    )
    assert not (
        color_events_check_report.rgbw_check_report.rgbw_value_check_report.validation
    )
