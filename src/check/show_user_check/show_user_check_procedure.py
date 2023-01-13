from ...migration.show_user.show_user import *
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from .show_user_check_report import *


def apply_takeoff_check(
    drone_user: DroneUser,
    takeoff_check_report: TakeoffCheckReport,
) -> None:
    # TODO:place a test on that
    if drone_user.nb_position_events == 0:
        takeoff_check_report.takeoff_duration_check_report.validation = False
        takeoff_check_report.takeoff_xyz_check_report.validation = False
    # TODO:place a test on that
    if drone_user.nb_position_events == 1:
        first_frame = drone_user.get_position_frame_by_index(0)
        first_position = drone_user.get_xyz_simulation_by_index(0)
        takeoff_check_report.takeoff_duration_check_report.validation = first_frame == 0
        takeoff_check_report.takeoff_xyz_check_report.validation = (
            first_position[2] == 0.0
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
