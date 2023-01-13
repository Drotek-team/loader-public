from ....migration.migration_dp_binary.drone_encoding_procedure import get_dance_size
from ....migration.show_px4.drone_px4.drone_px4 import DronePx4
from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ....report import Displayer


def apply_dance_size_check_procedure(
    drone_px4: DronePx4,
    dance_size_check_report: Displayer,
) -> None:
    dance_size_check_report.validation = (
        get_dance_size(drone_px4) < JSON_BINARY_PARAMETER.dance_size_max
    )
