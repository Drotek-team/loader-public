from ...show_user.drone_user.drone_user import DroneUser
from typing import List
from ...drones_px4.drones_px4 import DronesPx4, DronePx4
from .data_convertion_format import (
    XyzConvertionStandard,
    RgbwConvertionStandard,
    FireDurationConvertionStandard,
)


def drone_user_to_drone_px4_procedure(
    drone_user: DroneUser,
    xyz_convertion_standard: XyzConvertionStandard,
    rgbw_convertion_standard: RgbwConvertionStandard,
    fire_duration_convertion_standard: FireDurationConvertionStandard,
) -> DronePx4:
    drone_px4 = DronePx4()
    for position_event_user in drone_user.position_events:
        drone_px4.add_position(
            position_event_user.frame,
            xyz_convertion_standard.from_user_xyz_to_px4_xyz(
                position_event_user.xyz,
            ),
        )
    for color_event_user in drone_user.color_events:
        drone_px4.add_color(
            color_event_user.frame,
            rgbw_convertion_standard.from_user_rgbw_to_px4_rgbw(
                color_event_user.rgbw,
            ),
        )
    for fire_event_user in drone_user.fire_events:
        drone_px4.add_fire(
            fire_event_user.frame,
            fire_event_user.chanel,
            fire_duration_convertion_standard.from_user_fire_duration_to_px4_fire_duration(
                fire_event_user.duration
            ),
        )
    return drone_px4


def DU_to_DP_procedure(
    drones_user: List[DroneUser],
) -> DronesPx4:
    xyz_convertion_standard = XyzConvertionStandard()
    rgbw_convertion_standard = RgbwConvertionStandard()
    fire_duration_convertion_standard = FireDurationConvertionStandard()
    return DronesPx4(
        [
            drone_user_to_drone_px4_procedure(
                drone_user,
                xyz_convertion_standard,
                rgbw_convertion_standard,
                fire_duration_convertion_standard,
            )
            for drone_user in drones_user
        ]
    )
