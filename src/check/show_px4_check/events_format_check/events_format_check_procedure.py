from ....report import Contenor
from ....show_env.show_px4.drone_px4.drone_px4 import DronePx4
from ....show_env.show_px4.drone_px4.events.color_events import ColorEvents
from ....show_env.show_px4.drone_px4.events.fire_events import FireEvents
from ....show_env.show_px4.drone_px4.events.position_events import PositionEvents
from .events_format_check_tools import *


def position_events_check(
    position_events: PositionEvents,
) -> Contenor:
    position_events_contenor = Contenor("position_events")
    position_events_contenor.add_error_message(
        frame_check(
            position_events,
        )
    )
    position_events_contenor.add_error_message(
        xyz_check(
            position_events,
        )
    )
    return position_events_contenor


def color_events_check(
    color_events: ColorEvents,
) -> Contenor:
    color_events_contenor = Contenor("color_events")
    color_events_contenor.add_error_message(
        frame_check(
            color_events,
        )
    )
    color_events_contenor.add_error_message(
        rgbw_check(
            color_events,
        )
    )
    return color_events_contenor


def fire_events_check(
    fire_events: FireEvents,
) -> Contenor:
    fire_events_contenor = Contenor("fire_events")
    fire_events_contenor.add_error_message(
        frame_check(
            fire_events,
        )
    )
    fire_events_contenor.add_error_message(fire_chanel_check(fire_events))
    fire_events_contenor.add_error_message(
        fire_duration_frame_check(
            fire_events,
        )
    )
    return fire_events_contenor


def apply_events_format_check_procedure(
    drone: DronePx4,
) -> Contenor:
    events_format_contenor = Contenor("events_format")
    events_format_contenor.add_error_message(
        position_events_check(
            drone.position_events,
        )
    )
    events_format_contenor.add_error_message(
        color_events_check(
            drone.color_events,
        )
    )
    events_format_contenor.add_error_message(
        fire_events_check(
            drone.fire_events,
        )
    )
    return events_format_contenor
    return events_format_contenor
