from .....drones_px4.drone_px4.drone import DronePx4
from .....parameter.parameter import IostarParameter, JsonBinaryParameter
from ....json_conversion.json_convertion_tools.drone_encoding_procedure import (
    encode_drone,
)
from .dances_size_check_report import DanceSizeCheckReport


def apply_dance_size_check_procedure(
    drone: DronePx4,
    iostar_parameter: IostarParameter,
    json_binary_parameter: JsonBinaryParameter,
    dance_size_check_report: DanceSizeCheckReport,
) -> None:
    dance_size_check_report.validation = (
        len(
            encode_drone(
                drone,
                iostar_parameter,
                json_binary_parameter,
                dance_size_check_report.drone_encoding_report,
            )
        )
        < iostar_parameter.dance_size_max
    )
