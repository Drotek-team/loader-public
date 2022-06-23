from .....drones_manager.drone.drone import Drone
from .....drones_manager.drone.events.color_events import ColorEvents
from .....drones_manager.drone.events.fire_events import FireEvents
from .....drones_manager.drone.events.position_events import PositionEvents
from .....parameter.parameter import (
    IostarParameter,
    TakeoffParameter,
    TimecodeParameter,
)
from .events_format_check_report import (
    ColorEventsCheckReport,
    EventsFormatCheckReport,
    FireEventsCheckReport,
    PositionEventsCheckReport,
)
from .events_format_check_tools import (
    color_timecode_check,
    fire_chanel_check,
    fire_duration_check,
    fire_timecode_check,
    position_timecode_check,
    rgbw_check,
    takeoff_check,
    xyz_check,
)


def position_events_check(
    position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
    timecode_parameter: TimecodeParameter,
    iostar_parameters: IostarParameter,
    takeoff_parameter: TakeoffParameter,
) -> None:
    position_timecode_check(
        position_events,
        position_events_check_report.timecode_check_report,
        timecode_parameter,
    )
    xyz_check(
        position_events,
        position_events_check_report.xyz_check_report,
        iostar_parameters,
    )
    takeoff_check(
        position_events,
        position_events_check_report.takeoff_check_report,
        takeoff_parameter,
    )
    position_events_check_report.update()


def color_events_check(
    color_events: ColorEvents,
    color_events_check: ColorEventsCheckReport,
    timecode_parameter: TimecodeParameter,
    iostar_parameter: IostarParameter,
):
    color_timecode_check(
        color_events,
        color_events_check.timecode_check_report,
        timecode_parameter,
    )
    rgbw_check(color_events, color_events_check.rgbw_check_report, iostar_parameter)
    color_events_check.update()


def fire_events_check(
    fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
    timecode_parameter: TimecodeParameter,
    iostar_parameter: IostarParameter,
) -> None:
    fire_timecode_check(
        fire_events,
        fire_events_check_report.fire_timecode_check_report,
        timecode_parameter,
    )
    fire_chanel_check(
        fire_events, fire_events_check_report.fire_chanel_check_report, iostar_parameter
    )
    fire_duration_check(
        fire_events,
        fire_events_check_report.fire_duration_check_report,
        iostar_parameter,
    )
    fire_events_check_report.update()


def apply_events_format_check_procedure(
    drone: Drone,
    iostar_parameter: IostarParameter,
    takeoff_parameter: TakeoffParameter,
    timecode_parameter: TimecodeParameter,
    events_format_check_report: EventsFormatCheckReport,
):
    timecode_parameter = TimecodeParameter()
    takeoff_parameter = TakeoffParameter()
    position_events_check(
        drone.position_events,
        events_format_check_report.position_events_check,
        iostar_parameter,
        takeoff_parameter,
        timecode_parameter,
    )
    color_events_check(
        drone.color_events,
        events_format_check_report.color_events_check,
        iostar_parameter,
        timecode_parameter,
    )
    fire_events_check(
        drone.fire_events,
        events_format_check_report.fire_events_check,
        timecode_parameter,
        iostar_parameter,
    )

    events_format_check_report.position_events_check.update()
    events_format_check_report.color_events_check.update()
    events_format_check_report.fire_events_check.update()
