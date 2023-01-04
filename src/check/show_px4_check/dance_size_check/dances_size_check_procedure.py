from ....migration.migration_IJ_SP.migration_DP_binary.drone_encoding_procedure import (
    encode_drone,
)
from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ....show_px4.drone_px4.drone_px4 import DronePx4
from .dances_size_check_report import DanceSizeCheckReport


def apply_dance_size_check_procedure(
    drone: DronePx4,
    dance_size_check_report: DanceSizeCheckReport,
) -> None:
    dance_size_check_report.validation = (
        len(
            encode_drone(
                drone,
            )
        )
        < JSON_BINARY_PARAMETER.dance_size_max
    )
