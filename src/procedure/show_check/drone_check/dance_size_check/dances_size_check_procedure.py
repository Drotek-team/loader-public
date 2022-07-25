from .....drones_manager.drone.drone import DroneExport
from .....parameter.parameter import IostarParameter, JsonFormatParameter
from ....json_conversion.json_convertion_tools.drone_encoding_procedure import (
    encode_drone,
)
from .dances_size_check_report import DanceSizeCheckReport


def apply_dance_size_check_procedure(
    drone: DroneExport,
    iostar_parameter: IostarParameter,
    json_format_parameter: JsonFormatParameter,
    dance_size_check_report: DanceSizeCheckReport,
) -> None:
    dance_size_check_report.validation = (
        len(
            encode_drone(
                drone,
                json_format_parameter,
                dance_size_check_report.drone_encoding_report,
            )
        )
        < iostar_parameter.dance_size_max
    )
