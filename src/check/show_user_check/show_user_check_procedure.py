from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...show_user.show_user import DroneUser, ShowUser
from .show_user_check_report import (
    DroneUserCheckReport,
    IncoherenceRelativeAbsoluteFrame,
    ShowUserCheckReport,
)


def apply_drone_user_check_procedure(
    drone_user: DroneUser,
    drone_user_check_report: DroneUserCheckReport,
) -> None:
    # TO DO: An enum would be nice but it is kind of painfull because nothing here is make to make an enum
    # Fuck it just separate the three in the architecture, really not worth it
    for position_event in drone_user.position_events:
        if (
            position_event.absolute_frame
            != position_event.position_frame * FRAME_PARAMETER.position_fps
        ):
            drone_user_check_report.incoherence_relative_absolute_frame.append(
                IncoherenceRelativeAbsoluteFrame(
                    position_event.position_frame,
                    position_event.absolute_frame,
                    "position_event",
                    FRAME_PARAMETER.position_fps,
                )
            )
    for color_event in drone_user.color_events:
        if (
            color_event.absolute_frame
            != color_event.color_frame * FRAME_PARAMETER.color_fps
        ):
            drone_user_check_report.incoherence_relative_absolute_frame.append(
                IncoherenceRelativeAbsoluteFrame(
                    color_event.color_frame,
                    color_event.absolute_frame,
                    "color_event",
                    FRAME_PARAMETER.color_fps,
                )
            )

    for fire_event in drone_user.fire_events:
        if (
            fire_event.absolute_frame
            != fire_event.fire_frame * FRAME_PARAMETER.fire_fps
        ):
            drone_user_check_report.incoherence_relative_absolute_frame.append(
                IncoherenceRelativeAbsoluteFrame(
                    fire_event.fire_frame,
                    fire_event.absolute_frame,
                    "fire_event",
                    FRAME_PARAMETER.fire_fps,
                )
            )


def apply_show_user_check_procedure(
    show_user: ShowUser,
    show_user_check_report: ShowUserCheckReport,
) -> None:
    for drone_user, drone_user_check_report in zip(
        show_user.drones_user, show_user_check_report.drones_user_check_report
    ):
        apply_drone_user_check_procedure(drone_user, drone_user_check_report)
