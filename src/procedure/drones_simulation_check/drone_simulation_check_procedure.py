from ...show_simulation.drone_simulation import DroneSimulation
from .drone_simulation_check_report import (
    DroneSimulationCheckReport,
    TakeoffCheckReport,
)
from ...parameter.parameter import TakeoffParameter, FrameParameter


def takeoff_check(
    drone_simulation: DroneSimulation,
    takeoff_check_report: TakeoffCheckReport,
    takeoff_parameter: TakeoffParameter,
    frame_parameter: FrameParameter,
) -> None:
    if drone_simulation.nb_position_events_simulation == 0:
        takeoff_check_report.takeoff_duration_check_report.validation = False
        takeoff_check_report.takeoff_xyz_check_report.validation = False
    if drone_simulation.nb_position_events_simulation == 1:
        first_frame = drone_simulation.get_frame_by_index(0)
        first_position = drone_simulation.get_xyz_simulation_by_index(0)

        takeoff_check_report.takeoff_duration_check_report.validation = (
            takeoff_check_report.takeoff_xyz_check_report.validation
        ) = (first_frame == 0)
        takeoff_check_report.takeoff_xyz_check_report.validation = (
            first_position[2] == 0
        )
    if drone_simulation.nb_position_events_simulation > 1:
        first_frame = drone_simulation.get_frame_by_index(0)
        second_frame = drone_simulation.get_frame_by_index(1)
        first_position = drone_simulation.get_xyz_simulation_by_index(0)
        second_position = drone_simulation.get_xyz_simulation_by_index(1)

        takeoff_check_report.takeoff_duration_check_report.validation = (
            second_frame - first_frame
        ) == int(frame_parameter.json_fps * takeoff_parameter.takeoff_duration_second)
        takeoff_check_report.takeoff_xyz_check_report.validation = True
        takeoff_check_report.takeoff_xyz_check_report.validation = (
            first_position[0] == second_position[0]
            and first_position[1] == second_position[1]
            and takeoff_parameter.takeoff_altitude_meter + first_position[2]
            == second_position[2]
        )

    takeoff_check_report.update()


def apply_drone_simulation_check_procedure(
    drone_simulation: DroneSimulation,
    drone_simulation_check_report: DroneSimulationCheckReport,
    takeoff_parameter: TakeoffParameter,
    frame_parameter: FrameParameter,
) -> None:

    takeoff_check(
        drone_simulation,
        drone_simulation_check_report.takeoff_check_report,
        takeoff_parameter,
        frame_parameter,
    )
