from typing import List

from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.show_env.autopilot_format.drone_px4 import DronePx4
from loader.show_env.show_user import (
    ColorEventUser,
    DroneUser,
    FireEventUser,
    PositionEventUser,
    ShowUser,
)


def add_position_events_user(
    drone_px4: DronePx4,
    position_events_user: List[PositionEventUser],
) -> None:
    for position_event_user in position_events_user:
        drone_px4.add_position(
            JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
                position_event_user.frame,
            ),
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
            JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
                color_event_user.frame,
            ),
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
            JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
                fire_event_user.frame,
            ),
            fire_event_user.chanel,
            fire_event_user.duration,
        )


def drone_user_to_drone_px4(
    drone_user: DroneUser,
) -> DronePx4:
    drone_px4 = DronePx4(drone_user.index)
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


def su_to_sp(
    show_user: ShowUser,
) -> List[DronePx4]:
    return [
        drone_user_to_drone_px4(
            drone_user,
        )
        for drone_user in show_user.drones_user
    ]
