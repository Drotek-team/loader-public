from ...show_user.drone_user.drone_user import (
    DroneUser,
    PositionEventUser,
    ColorEventUser,
    FireEventUser,
)
from ...show_px4.show_px4 import ShowPx4, DronePx4
from .data_convertion_format import (
    XyzConvertionStandard,
    RgbwConvertionStandard,
    FireDurationConvertionStandard,
)
from ...show_user.show_user import ShowUser


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
                position_event_px4.xyz
            ),
        )
        for position_event_px4 in drone_px4.position_events.events
    ]
    color_events_user = [
        ColorEventUser(
            frame=color_event_px4.frame,
            rgbw=rgbw_convertion_standard.from_px4_rgbw_to_user_rgbw(
                color_event_px4.rgbw
            ),
        )
        for color_event_px4 in drone_px4.color_events.events
    ]

    fire_events_user = [
        FireEventUser(
            frame=fire_event_px4.frame,
            chanel=fire_event_px4.chanel,
            duration=fire_duration_convertion_standard.from_px4_fire_duration_to_user_fire_duration(
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
    xyz_convertion_standard = XyzConvertionStandard()
    rgbw_convertion_standard = RgbwConvertionStandard()
    fire_duration_convertion_standard = FireDurationConvertionStandard()
    return ShowUser(
        drones_user=[
            drone_px4_to_drone_user_procedure(
                drone_px4,
                xyz_convertion_standard,
                rgbw_convertion_standard,
                fire_duration_convertion_standard,
            )
            for drone_px4 in show_px4
        ]
    )