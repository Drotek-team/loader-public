from ....drones_manager.drone.drone import Drone
from ....parameter.parameter import Parameter
from .dance_size_check.dances_size_check_procedure import (
    apply_dance_size_check_procedure,
)
from .drone_check_report import DroneCheckReport
from .events_format_check.events_format_check_procedure import (
    apply_events_format_check_procedure,
)


def apply_drone_check_procedure(
    drone: Drone, drone_check_report: DroneCheckReport, parameter: Parameter
) -> None:
    apply_events_format_check_procedure(
        drone,
        drone_check_report.events_format_check_report,
        parameter.takeoff_parameter,
        parameter.timecode_parameter,
    )
    apply_dance_size_check_procedure(
        drone, drone_check_report.dance_size_check_report, parameter.iostar_parameter
    )
