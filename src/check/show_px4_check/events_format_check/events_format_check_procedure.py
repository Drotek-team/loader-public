from ....show_px4.drone_px4.drone_px4 import DronePx4
from ....show_px4.drone_px4.events.color_events import ColorEvents
from ....show_px4.drone_px4.events.fire_events import FireEvents
from ....show_px4.drone_px4.events.position_events import PositionEvents
from .events_format_check_report import *
from .events_format_check_tools import *


def position_events_check(
    position_events: PositionEvents,
    position_events_check_report: PositionEventsCheckReport,
) -> None:
    position_frame_check(
        position_events,
        position_events_check_report.frame_check_report,
    )
    xyz_check(
        position_events,
        position_events_check_report.xyz_check_report,
    )
    position_events_check_report.update_contenor_validation


def color_events_check(
    color_events: ColorEvents,
    color_events_check_report: ColorEventsCheckReport,
):
    color_frame_check(
        color_events,
        color_events_check_report.frame_check_report,
    )
    rgbw_check(color_events, color_events_check_report.rgbw_check_report)
    color_events_check_report.update_contenor_validation


def fire_events_check(
    fire_events: FireEvents,
    fire_events_check_report: FireEventsCheckReport,
) -> None:
    fire_frame_check(
        fire_events,
        fire_events_check_report.fire_frame_check_report,
    )
    fire_chanel_check(fire_events, fire_events_check_report.fire_chanel_check_report)
    fire_duration_frame_check(
        fire_events,
        fire_events_check_report.fire_duration_check_report,
    )
    fire_events_check_report.update_contenor_validation


def apply_events_format_check_procedure(
    drone: DronePx4,
    events_format_check_report: EventsFormatCheckReport,
):
    position_events_check(
        drone.position_events,
        events_format_check_report.position_events_check,
    )
    color_events_check(
        drone.color_events,
        events_format_check_report.color_events_check,
    )
    fire_events_check(
        drone.fire_events,
        events_format_check_report.fire_events_check,
    )

    events_format_check_report.update_contenor_validation
