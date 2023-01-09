from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ...show_px4.show_px4 import DronePx4, ShowPx4
from ...show_user.show_user import *


def drone_px4_to_drone_user_procedure(
    drone_px4: DronePx4,
) -> DroneUser:
    position_events_user = [
        PositionEventUser(
            frame=position_event_px4.frame,
            xyz=JSON_BINARY_PARAMETER.from_px4_xyz_to_user_xyz(position_event_px4.xyz),
        )
        for position_event_px4 in drone_px4.position_events.events
    ]
    color_events_user = [
        ColorEventUser(
            frame=color_event_px4.frame,
            rgbw=JSON_BINARY_PARAMETER.from_px4_rgbw_to_user_rgbw(color_event_px4.rgbw),
        )
        for color_event_px4 in drone_px4.color_events.events
    ]

    fire_events_user = [
        FireEventUser(
            frame=fire_event_px4.frame,
            chanel=fire_event_px4.chanel,
            duration=JSON_BINARY_PARAMETER.from_px4_fire_duration_to_user_fire_duration(
                fire_event_px4.duration
            ),
        )
        for fire_event_px4 in drone_px4.fire_events.events
    ]

    return DroneUser(
        position_events=position_events_user,
        color_events=color_events_user,
        fire_events=fire_events_user,
    )


def SP_to_SU_procedure(
    show_px4: ShowPx4,
) -> ShowUser:
    return ShowUser(
        drones_user=[
            drone_px4_to_drone_user_procedure(
                drone_px4,
            )
            for drone_px4 in show_px4
        ]
    )
