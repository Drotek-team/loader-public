from ....drones_px4.drone_px4.drone_px4 import DronePx4
from ....drones_px4.drone_px4.events.color_events import ColorEvents
from ....drones_px4.drone_px4.events.fire_events import FireEvents
from ....drones_px4.drone_px4.events.position_events import PositionEvents
from ....parameter.parameter import (
    IostarParameter,
    TakeoffParameter,
    FrameParameter,
)
from .events_format_check_report import (
    ColorEventsCheckReport,
    EventsFormatCheckReport,
    FireEventsCheckReport,
    PositionEventsCheckReport,
)
from .events_format_check_tools import (
    color_frame_check,
    fire_chanel_check,
    fire_duration_frame_check,
    fire_frame_check,
    position_frame_check,
    rgbw_check,
    takeoff_check,
    xyz_check,
)


def position_events_check(
    position_events: PositionEvents,
    frame_parameter: FrameParameter,
    iostar_parameter: IostarParameter,
    takeoff_parameter: TakeoffParameter,
    position_events_check_report: PositionEventsCheckReport,
) -> None:
    position_frame_check(
        position_events,
        position_events_check_report.frame_check_report,
        frame_parameter,
    )
    xyz_check(
        position_events,
        position_events_check_report.xyz_check_report,
        iostar_parameter,
    )
    takeoff_check(
        position_events,
        takeoff_parameter,
        frame_parameter,
        position_events_check_report.takeoff_check_report,
    )
    position_events_check_report.update()


def color_events_check(
    color_events: ColorEvents,
    frame_parameter: FrameParameter,
    iostar_parameter: IostarParameter,
    color_events_check_report: ColorEventsCheckReport,
):
    color_frame_check(
        color_events,
        color_events_check_report.frame_check_report,
        frame_parameter,
    )
    rgbw_check(
        color_events, color_events_check_report.rgbw_check_report, iostar_parameter
    )
    color_events_check_report.update()


def fire_events_check(
    fire_events: FireEvents,
    frame_parameter: FrameParameter,
    iostar_parameter: IostarParameter,
    fire_events_check_report: FireEventsCheckReport,
) -> None:
    fire_frame_check(
        fire_events,
        fire_events_check_report.fire_frame_check_report,
        frame_parameter,
    )
    fire_chanel_check(
        fire_events, fire_events_check_report.fire_chanel_check_report, iostar_parameter
    )
    fire_duration_frame_check(
        fire_events,
        fire_events_check_report.fire_duration_check_report,
        iostar_parameter,
    )
    fire_events_check_report.update()


def apply_events_format_check_procedure(
    drone: DronePx4,
    iostar_parameter: IostarParameter,
    takeoff_parameter: TakeoffParameter,
    frame_parameter: FrameParameter,
    events_format_check_report: EventsFormatCheckReport,
):
    position_events_check(
        drone.position_events,
        frame_parameter,
        iostar_parameter,
        takeoff_parameter,
        events_format_check_report.position_events_check,
    )
    color_events_check(
        drone.color_events,
        frame_parameter,
        iostar_parameter,
        events_format_check_report.color_events_check,
    )
    fire_events_check(
        drone.fire_events,
        frame_parameter,
        iostar_parameter,
        events_format_check_report.fire_events_check,
    )

    events_format_check_report.position_events_check.update()
    events_format_check_report.color_events_check.update()
    events_format_check_report.fire_events_check.update()
    events_format_check_report.update()
