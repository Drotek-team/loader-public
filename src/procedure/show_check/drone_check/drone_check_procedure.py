from ....drones_manager.drone.drone import DroneExport
from ....parameter.parameter import Parameter
from .dance_size_check.dances_size_check_procedure import (
    apply_dance_size_check_procedure,
)
from .drone_check_report import DroneCheckReport
from .events_format_check.events_format_check_procedure import (
    apply_events_format_check_procedure,
)


def apply_drone_check_procedure(
    drone: DroneExport, drone_check_report: DroneCheckReport, parameter: Parameter
) -> None:
    apply_events_format_check_procedure(
        drone,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        parameter.timecode_parameter,
        drone_check_report.events_format_check_report,
    )
    apply_dance_size_check_procedure(
        drone,
        parameter.iostar_parameter,
        parameter.json_format_parameter,
        drone_check_report.dance_size_check_report,
    )
    drone_check_report.update()
