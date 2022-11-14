from ....migration.migration_IJ_SP.migration_DP_binary.drone_encoding_procedure import (
    encode_drone,
)
from ....parameter.parameter import IostarParameter, JsonBinaryParameter
from ....show_px4.drone_px4.drone_px4 import DronePx4
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
                json_binary_parameter,
            )
        )
        < iostar_parameter.dance_size_max
    )
