from ....report import Contenor
from ....show_env.show_px4.drone_px4.drone_px4 import DronePx4
from ....show_env.show_px4.drone_px4.events.color_events import ColorEvents
from ....show_env.show_px4.drone_px4.events.fire_events import FireEvents
from ....show_env.show_px4.drone_px4.events.position_events import PositionEvents
from .events_format_check_tools import (
    chromes_value_check,
    coordinates_value_check,
    fire_chanel_duration_check,
    timecodes_check,
)


def position_events_check(
    position_events: PositionEvents,
) -> Contenor:
    position_events_contenor = Contenor("position_events")
    position_events_contenor.add_error_message(
        timecodes_check(
            position_events,
        )
    )
    position_events_contenor.add_error_message(
        coordinates_value_check(
            position_events,
        )
    )
    return position_events_contenor


def color_events_check(
    color_events: ColorEvents,
) -> Contenor:
    color_events_contenor = Contenor("color_events")
    color_events_contenor.add_error_message(
        timecodes_check(
            color_events,
        )
    )
    color_events_contenor.add_error_message(
        chromes_value_check(
            color_events,
        )
    )
    return color_events_contenor


def fire_events_check(
    fire_events: FireEvents,
) -> Contenor:
    fire_events_contenor = Contenor("fire_events")
    fire_events_contenor.add_error_message(
        timecodes_check(
            fire_events,
        )
    )
    fire_events_contenor.add_error_message(fire_chanel_duration_check(fire_events))
    return fire_events_contenor


def apply_events_format_check(
    drone_px4: DronePx4,
) -> Contenor:
    events_format_contenor = Contenor(f"Drone {drone_px4.index} events format")
    events_format_contenor.add_error_message(
        position_events_check(
            drone_px4.position_events,
        )
    )
    events_format_contenor.add_error_message(
        color_events_check(
            drone_px4.color_events,
        )
    )
    events_format_contenor.add_error_message(
        fire_events_check(
            drone_px4.fire_events,
        )
    )
    return events_format_contenor
