from ...show_user.show_user import ShowUser, DroneUser
from .show_user_check_report import (
    ShowUserCheckReport,
    DroneUserCheckReport,
    IncoherenceRelativeAbsoluteFrame,
)
from ...parameter.parameter import FrameParameter


def apply_drone_user_check_procedure(
    drone_user: DroneUser,
    drone_user_check_report: DroneUserCheckReport,
    frame_parameter: FrameParameter,
) -> None:
    ### TO DO: An enum would be nice but it is kind of painfull because nothing here is make to make an enum
    ### Fuck it just separate the three in the architecture, really not worth it
    for position_event in drone_user.position_events:
        if (
            position_event.absolute_frame
            != position_event.position_frame * frame_parameter.position_fps
        ):
            drone_user_check_report.incoherence_relative_absolute_frame.append(
                IncoherenceRelativeAbsoluteFrame(
                    position_event.position_frame,
                    position_event.absolute_frame,
                    "position_event",
                    frame_parameter.position_fps,
                )
            )
    for color_event in drone_user.color_events:
        if (
            color_event.absolute_frame
            != color_event.color_frame * frame_parameter.color_fps
        ):
            drone_user_check_report.incoherence_relative_absolute_frame.append(
                IncoherenceRelativeAbsoluteFrame(
                    color_event.color_frame,
                    color_event.absolute_frame,
                    "color_event",
                    frame_parameter.color_fps,
                )
            )

    for fire_event in drone_user.fire_events:
        if (
            fire_event.absolute_frame
            != fire_event.fire_frame * frame_parameter.fire_fps
        ):
            drone_user_check_report.incoherence_relative_absolute_frame.append(
                IncoherenceRelativeAbsoluteFrame(
                    fire_event.fire_frame,
                    fire_event.absolute_frame,
                    "fire_event",
                    frame_parameter.fire_fps,
                )
            )


def apply_show_user_check_procedure(
    show_user: ShowUser,
    show_user_check_report: ShowUserCheckReport,
    frame_parameter: FrameParameter,
) -> None:
    for drone_user, drone_user_check_report in zip(
        show_user.drones_user, show_user_check_report.drones_user_check_report
    ):
        apply_drone_user_check_procedure(
            drone_user, drone_user_check_report, frame_parameter
        )
