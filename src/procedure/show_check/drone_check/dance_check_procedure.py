from ....drones_user.drone.drone import DroneExport
from ....parameter.parameter import Parameter
from .dance_size_check.dances_size_check_procedure import (
    apply_dance_size_check_procedure,
)
from .dance_check_report import DanceCheckReport
from .events_format_check.events_format_check_procedure import (
    apply_events_format_check_procedure,
)


def apply_dance_check_procedure(
    drone: DroneExport, dance_check_report: DanceCheckReport, parameter: Parameter
) -> None:
    apply_events_format_check_procedure(
        drone,
        parameter.iostar_parameter,
        parameter.takeoff_parameter,
        parameter.frame_parameter,
        parameter.json_convertion_constant,
        dance_check_report.events_format_check_report,
    )
    apply_dance_size_check_procedure(
        drone,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        dance_check_report.dance_size_check_report,
    )
    dance_check_report.update()
