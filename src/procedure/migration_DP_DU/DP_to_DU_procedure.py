from ...show_user.drone_user.drone_user import (
    DroneUser,
    PositionEventUser,
    ColorEventUser,
    FireEventUser,
)
from typing import List
from ...drones_px4.drones_px4 import DronesPx4, DronePx4
from .data_convertion_format import (
    XyzConvertionStandard,
    RgbwConvertionStandard,
    FireDurationConvertionStandard,
)


def drone_px4_to_drone_user_procedure(
    drone_px4: DronePx4,
    xyz_convertion_standard: XyzConvertionStandard,
    rgbw_convertion_standard: RgbwConvertionStandard,
    fire_duration_convertion_standard: FireDurationConvertionStandard,
) -> DroneUser:
    position_events_user = [
        PositionEventUser(
            frame=position_event_px4.frame,
            xyz=xyz_convertion_standard.from_px4_xyz_to_user_xyz(
                position_event_px4.get_values()
            ),
        )
        for position_event_px4 in drone_px4.position_events.event_list
    ]
    color_events_user = [
        ColorEventUser(
            frame=color_event_px4.frame,
            rgbw=rgbw_convertion_standard.from_px4_rgbw_to_user_rgbw(
                color_event_px4.get_values()
            ),
        )
        for color_event_px4 in drone_px4.color_events.event_list
    ]

    fire_events_user = [
        FireEventUser(
            frame=fire_event_px4.frame,
            chanel=fire_event_px4.get_values()[0],
            duration=fire_duration_convertion_standard.from_px4_fire_duration_to_user_fire_duration(
                fire_event_px4.get_values()[1]
            ),
        )
        for fire_event_px4 in drone_px4.fire_events.event_list
    ]

    return DroneUser(
        position_events=position_events_user,
        color_events=color_events_user,
        fire_events=fire_events_user,
    )


def DU_to_DP_procedure(
    drones_px4: DronesPx4,
) -> List[DroneUser]:
    xyz_convertion_standard = XyzConvertionStandard()
    rgbw_convertion_standard = RgbwConvertionStandard()
    fire_duration_convertion_standard = FireDurationConvertionStandard()
    return DronesPx4(
        [
            drone_px4_to_drone_user_procedure(
                drone_px4,
                xyz_convertion_standard,
                rgbw_convertion_standard,
                fire_duration_convertion_standard,
            )
            for drone_px4 in drones_px4
        ]
    )
