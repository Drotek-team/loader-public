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
    ColorEventsCheck,
    EventsFormatCheckReport,
    FireEventsCheck,
    PositionEventsCheck,
)
from .events_format_check_tools import (
    fire_chanel_check,
    fire_duration_check,
    rgbw_check,
    takeoff_check,
    timecode_check,
    xyz_check,
)


def position_events_check(
    position_events: PositionEvents,
    position_events_check: PositionEventsCheck,
    timecode_parameter: TimecodeParameter,
    iostar_parameters: IostarParameter,
    takeoff_parameter: TakeoffParameter,
) -> None:
    timecodes = [event.timecode for event in position_events.events]
    positions = [event.get_values() for event in position_events.events]
    position_events_check.timecode_check.update(
        timecode_check(
            timecodes,
            timecode_parameter.position_frequence,
            timecode_parameter.show_time_begin,
        )
    )
    position_events_check.xyz_check.update(xyz_check(positions, iostar_parameters))
    position_events_check.takeoff_check.update(
        takeoff_check(
            position_events,
            takeoff_parameter.takeoff_altitude,
            takeoff_parameter.takeoff_duration,
        )
    )


def color_events_check(
    color_events: ColorEvents,
    color_events_check: ColorEventsCheck,
    timecode_parameter: TimecodeParameter,
    iostar_parameter: IostarParameter,
):
    timecodes = [event.timecode for event in color_events.events]
    colors = [event.get_values() for event in color_events.events]
    color_events_check.timecode_check.update(
        timecode_check(
            timecodes,
            timecode_parameter.color_frequence,
            timecode_parameter.show_time_begin,
        )
    )
    color_events_check.rgbw_check.update(rgbw_check(colors, iostar_parameter))


def fire_events_check(
    fire_events: FireEvents,
    fire_events_check: FireEventsCheck,
    timecode_parameter: TimecodeParameter,
    iostar_parameter: IostarParameter,
):
    timecodes = [event.timecode for event in fire_events.events]
    fire_chanels = [event.get_values()[0] for event in fire_events.events]
    fire_durations = [event.get_values()[1] for event in fire_events.events]
    fire_events_check.timecode_check.update(
        timecode_check(
            timecodes,
            timecode_parameter.color_frequence,
            timecode_parameter.show_time_begin,
        )
    )
    fire_events_check.fire_chanel_check.update(
        fire_chanel_check(fire_chanels, iostar_parameter)
    )
    fire_events_check.fire_duration_check.update(
        fire_duration_check(fire_durations, iostar_parameter)
    )


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
