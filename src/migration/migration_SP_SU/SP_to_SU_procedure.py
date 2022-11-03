from ...show_user.show_user import (
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
from ...parameter.parameter import FrameParameter


def drone_px4_to_drone_user_procedure(
    drone_px4: DronePx4,
    xyz_convertion_standard: XyzConvertionStandard,
    rgbw_convertion_standard: RgbwConvertionStandard,
    fire_duration_convertion_standard: FireDurationConvertionStandard,
    frame_parameter: FrameParameter,
) -> DroneUser:
    position_events_user = [
        PositionEventUser(
            position_frame=position_event_px4.frame,
            absolute_frame=frame_parameter.from_position_frame_to_json_frame(
                position_event_px4.frame
            ),
            xyz=xyz_convertion_standard.from_px4_xyz_to_user_xyz(
                position_event_px4.xyz
            ),
        )
        for position_event_px4 in drone_px4.position_events.events
    ]
    color_events_user = [
        ColorEventUser(
            color_frame=color_event_px4.frame,
            absolute_frame=frame_parameter.from_color_frame_to_json_frame(
                color_event_px4.frame
            ),
            rgbw=rgbw_convertion_standard.from_px4_rgbw_to_user_rgbw(
                color_event_px4.rgbw
            ),
        )
        for color_event_px4 in drone_px4.color_events.events
    ]

    fire_events_user = [
        FireEventUser(
            fire_frame=fire_event_px4.frame,
            absolute_frame=frame_parameter.from_fire_frame_to_json_frame(
                fire_event_px4.frame
            ),
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
    frame_parameter: FrameParameter,
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
                frame_parameter,
            )
            for drone_px4 in show_px4
        ]
    )
