from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...show_dev.show_dev import DroneDev, ShowDev
from .show_dev_check_report import ShowDevCheckReport, TakeoffCheckReport


def takeoff_check(
    drone_dev: DroneDev,
    takeoff_check_report: TakeoffCheckReport,
) -> None:
    if drone_dev.nb_position_events_dev == 0:
        takeoff_check_report.takeoff_duration_check_report.validation = False
        takeoff_check_report.takeoff_xyz_check_report.validation = False
    if drone_dev.nb_position_events_dev == 1:
        first_frame = drone_dev.get_frame_by_index(0)
        first_position = drone_dev.get_xyz_simulation_by_index(0)

        takeoff_check_report.takeoff_duration_check_report.validation = (
            takeoff_check_report.takeoff_xyz_check_report.validation
        ) = (first_frame == 0)
        takeoff_check_report.takeoff_xyz_check_report.validation = (
            first_position[2] == 0
        )
    if drone_dev.nb_position_events_dev > 1:
        first_frame = drone_dev.get_frame_by_index(0)
        second_frame = drone_dev.get_frame_by_index(1)
        first_position = drone_dev.get_xyz_simulation_by_index(0)
        second_position = drone_dev.get_xyz_simulation_by_index(1)

        takeoff_check_report.takeoff_duration_check_report.validation = (
            second_frame - first_frame
        ) == int(
            FRAME_PARAMETER.absolute_fps * TAKEOFF_PARAMETER.takeoff_duration_second
        )
        takeoff_check_report.takeoff_xyz_check_report.validation = True
        takeoff_check_report.takeoff_xyz_check_report.validation = (
            first_position[0] == second_position[0]
            and first_position[1] == second_position[1]
            and TAKEOFF_PARAMETER.takeoff_altitude_meter + first_position[2]
            == second_position[2]
        )

    takeoff_check_report.update()


def apply_show_dev_procedure(
    show_dev: ShowDev,
    show_dev_check_report: ShowDevCheckReport,
) -> None:
    for drone_dev, drone_dev_check_report in zip(
        show_dev.drones_dev, show_dev_check_report.drones_dev_check_report
    ):
        takeoff_check(
            drone_dev,
            drone_dev_check_report.takeoff_check_report,
        )
        drone_dev_check_report.update()
    show_dev_check_report.update()
