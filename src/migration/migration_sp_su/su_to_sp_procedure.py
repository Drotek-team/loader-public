from typing import List

from ...parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ...show_px4.show_px4 import *
from ...show_user.show_user import *


def add_position_events_user(
    drone_px4: DronePx4,
    position_events_user: List[PositionEventUser],
) -> None:
    for position_event_user in position_events_user:
        drone_px4.add_position(
            position_event_user.frame,
            JSON_BINARY_PARAMETER.from_user_xyz_to_px4_xyz(
                position_event_user.xyz,
            ),
        )


def add_color_events_user(
    drone_px4: DronePx4,
    color_events_user: List[ColorEventUser],
) -> None:
    for color_event_user in color_events_user:
        drone_px4.add_color(
            color_event_user.frame,
            JSON_BINARY_PARAMETER.from_user_rgbw_to_px4_rgbw(
                color_event_user.rgbw,
            ),
        )


def add_fire_events_user(
    drone_px4: DronePx4,
    fire_events_user: List[FireEventUser],
) -> None:
    for fire_event_user in fire_events_user:
        drone_px4.add_fire(
            fire_event_user.frame,
            fire_event_user.chanel,
            JSON_BINARY_PARAMETER.from_user_fire_duration_to_px4_fire_duration(
                fire_event_user.duration
            ),
        )


def drone_user_to_drone_px4_procedure(
    drone_user: DroneUser,
    drone_index: int,
) -> DronePx4:
    drone_px4 = DronePx4(drone_index)
    add_position_events_user(drone_px4, drone_user.position_events)
    add_color_events_user(
        drone_px4,
        drone_user.color_events,
    )
    add_fire_events_user(
        drone_px4,
        drone_user.fire_events,
    )
    return drone_px4


def su_to_sp_procedure(
    show_user: ShowUser,
) -> ShowPx4:
    return ShowPx4(
        [
            drone_user_to_drone_px4_procedure(
                drone_user,
                drone_index,
            )
            for drone_index, drone_user in enumerate(show_user.drones_user)
        ]
    )
