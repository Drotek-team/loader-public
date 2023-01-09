from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...show_user.show_user import *
from .show_user_check_report import *


def get_incoherence_frame_absolute_time_name(
    frame: int, absolute_time: float, event_type: str, event_fps: int
) -> str:
    return f"Frame {frame} at {absolute_time} is not coherent with {event_type} at {event_fps} fps"


def apply_drone_user_frame_coherence_check(
    drone_user: DroneUser, frame_coherence_check_report: FrameCoherenceCheckReport
) -> None:
    # IMPROVE: An enum would be nice but it is kind of painfull because nothing here is make to make an enum
    for position_event in drone_user.position_events:
        if (
            position_event.absolute_time
            != FRAME_PARAMETER.from_position_frame_to_absolute_time(
                position_event.position_frame
            )
        ):
            frame_coherence_check_report.incoherence_relative_absolute_time.append(
                Displayer(
                    get_incoherence_frame_absolute_time_name(
                        position_event.position_frame,
                        position_event.absolute_time,
                        "position event",
                        FRAME_PARAMETER.position_fps,
                    )
                )
            )
    for color_event in drone_user.color_events:
        if (
            color_event.absolute_time
            != FRAME_PARAMETER.from_color_frame_to_absolute_time(
                color_event.color_frame
            )
        ):
            frame_coherence_check_report.incoherence_relative_absolute_time.append(
                Displayer(
                    get_incoherence_frame_absolute_time_name(
                        color_event.color_frame,
                        color_event.absolute_time,
                        "color event",
                        FRAME_PARAMETER.color_fps,
                    )
                )
            )

    for fire_event in drone_user.fire_events:
        if (
            fire_event.absolute_time
            != FRAME_PARAMETER.from_fire_frame_to_absolute_time(fire_event.fire_frame)
        ):
            frame_coherence_check_report.incoherence_relative_absolute_time.append(
                Displayer(
                    get_incoherence_frame_absolute_time_name(
                        fire_event.fire_frame,
                        fire_event.absolute_time,
                        "fire event",
                        FRAME_PARAMETER.fire_fps,
                    )
                )
            )
    frame_coherence_check_report.update_contenor_validation()


def apply_takeoff_check(
    drone_user: DroneUser,
    takeoff_check_report: TakeoffCheckReport,
) -> None:
    if drone_user.nb_position_events == 0:
        takeoff_check_report.takeoff_duration_check_report.validation = False
        takeoff_check_report.takeoff_xyz_check_report.validation = False
    if drone_user.nb_position_events == 1:
        first_frame = drone_user.get_position_frame_by_index(0)
        first_position = drone_user.get_xyz_simulation_by_index(0)

        takeoff_check_report.takeoff_duration_check_report.validation = (
            takeoff_check_report.takeoff_xyz_check_report.validation
        ) = (first_frame == 0)
        takeoff_check_report.takeoff_xyz_check_report.validation = (
            first_position[2] == 0
        )
    if drone_user.nb_position_events > 1:
        first_time = drone_user.get_absolute_time_by_index(0)
        second_time = drone_user.get_absolute_time_by_index(1)
        first_position = drone_user.get_xyz_simulation_by_index(0)
        second_position = drone_user.get_xyz_simulation_by_index(1)
        takeoff_check_report.takeoff_duration_check_report.validation = (
            second_time - first_time
        ) == TAKEOFF_PARAMETER.takeoff_duration_second
        takeoff_check_report.takeoff_xyz_check_report.validation = (
            first_position[0] == second_position[0]
            and first_position[1] == second_position[1]
            and first_position[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter_min
            <= second_position[2]
            and second_position[2]
            <= first_position[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter_max
        )
    takeoff_check_report.update_contenor_validation()


def apply_drone_user_check_procedure(
    drone_user: DroneUser,
    drone_user_check_report: DroneUserCheckReport,
) -> None:
    apply_drone_user_frame_coherence_check(
        drone_user, drone_user_check_report.frame_coherence_check_report
    )
    apply_takeoff_check(drone_user, drone_user_check_report.takeoff_check_report)
    drone_user_check_report.update_contenor_validation()


def apply_show_user_check_procedure(
    show_user: ShowUser,
    show_user_check_report: ShowUserCheckReport,
) -> None:
    for drone_user, drone_user_check_report in zip(
        show_user.drones_user, show_user_check_report.drones_user_check_report
    ):
        apply_drone_user_check_procedure(drone_user, drone_user_check_report)
    show_user_check_report.update_contenor_validation()
