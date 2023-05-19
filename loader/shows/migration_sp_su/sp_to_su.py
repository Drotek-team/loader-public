from typing import List

from loader.parameters import JSON_BINARY_PARAMETERS
from loader.shows.drone_px4 import DronePx4
from loader.shows.show_user import (
    ColorEventUser,
    DroneUser,
    FireEventUser,
    PositionEventUser,
    ShowUser,
)


def drone_px4_to_drone_user(
    drone_px4: DronePx4,
) -> DroneUser:
    position_events_user = [
        PositionEventUser(
            frame=JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(
                position_event_px4.timecode,
            ),
            xyz=JSON_BINARY_PARAMETERS.from_px4_xyz_to_user_xyz(position_event_px4.xyz),
        )
        for position_event_px4 in drone_px4.position_events.specific_events
    ]
    color_events_user = [
        ColorEventUser(
            frame=JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(
                color_event_px4.timecode,
            ),
            rgbw=JSON_BINARY_PARAMETERS.from_px4_rgbw_to_user_rgbw(color_event_px4.rgbw),
        )
        for color_event_px4 in drone_px4.color_events.specific_events
    ]

    fire_events_user = [
        FireEventUser(
            frame=JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(
                fire_event_px4.timecode,
            ),
            chanel=fire_event_px4.chanel,
            duration=fire_event_px4.duration,
        )
        for fire_event_px4 in drone_px4.fire_events.specific_events
    ]

    return DroneUser(
        index=drone_px4.index,
        position_events=position_events_user,
        color_events=color_events_user,
        fire_events=fire_events_user,
    )


def sp_to_su(
    autopilot_format: List[DronePx4],
) -> ShowUser:
    return ShowUser(
        drones_user=[
            drone_px4_to_drone_user(
                drone_px4,
            )
            for drone_px4 in autopilot_format
        ],
    )
