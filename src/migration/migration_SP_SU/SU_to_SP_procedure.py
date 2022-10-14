from ...show_user.show_user import (
    DroneUser,
    PositionEventUser,
    ColorEventUser,
    FireEventUser,
)
from ...show_user.show_user import ShowUser
from typing import List
from ...show_px4.show_px4 import ShowPx4, DronePx4
from .data_convertion_format import (
    XyzConvertionStandard,
    RgbwConvertionStandard,
    FireDurationConvertionStandard,
)
from typing import List


def add_position_events_user(
    drone_px4: DronePx4,
    position_events_user: List[PositionEventUser],
    xyz_convertion_standard: XyzConvertionStandard,
) -> None:
    for position_event_user in position_events_user:
        ### URGENT: do something for that
        drone_px4.add_position(
            6 * position_event_user.position_frame,
            xyz_convertion_standard.from_user_xyz_to_px4_xyz(
                position_event_user.xyz,
            ),
        )


def add_color_events_user(
    drone_px4: DronePx4,
    color_events_user: List[ColorEventUser],
    rgbw_convertion_standard: RgbwConvertionStandard,
) -> None:
    for color_event_user in color_events_user:
        drone_px4.add_color(
            color_event_user.color_frame,
            rgbw_convertion_standard.from_user_rgbw_to_px4_rgbw(
                color_event_user.rgbw,
            ),
        )


def add_fire_events_user(
    drone_px4: DronePx4,
    fire_events_user: List[FireEventUser],
    fire_duration_convertion_standard: FireDurationConvertionStandard,
) -> None:
    for fire_event_user in fire_events_user:
        drone_px4.add_fire(
            fire_event_user.fire_frame,
            fire_event_user.chanel,
            fire_duration_convertion_standard.from_user_fire_duration_to_px4_fire_duration(
                fire_event_user.duration
            ),
        )


def drone_user_to_drone_px4_procedure(
    drone_user: DroneUser,
    drone_index: int,
    xyz_convertion_standard: XyzConvertionStandard,
    rgbw_convertion_standard: RgbwConvertionStandard,
    fire_duration_convertion_standard: FireDurationConvertionStandard,
) -> DronePx4:
    drone_px4 = DronePx4(drone_index)
    add_position_events_user(
        drone_px4, drone_user.position_events, xyz_convertion_standard
    )
    add_color_events_user(
        drone_px4,
        drone_user.color_events,
        rgbw_convertion_standard,
    )
    add_fire_events_user(
        drone_px4,
        drone_user.fire_events,
        fire_duration_convertion_standard,
    )
    return drone_px4


def SU_to_SP_procedure(
    show_user: ShowUser,
) -> ShowPx4:
    xyz_convertion_standard = XyzConvertionStandard()
    rgbw_convertion_standard = RgbwConvertionStandard()
    fire_duration_convertion_standard = FireDurationConvertionStandard()
    return ShowPx4(
        [
            drone_user_to_drone_px4_procedure(
                drone_user,
                drone_index,
                xyz_convertion_standard,
                rgbw_convertion_standard,
                fire_duration_convertion_standard,
            )
            for drone_index, drone_user in enumerate(show_user.drones_user)
        ]
    )
