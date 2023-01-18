from ....parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from ....report import Displayer
from ....show_env.migration_dp_binary.drone_encoding_procedure import get_dance_size
from ....show_env.show_px4.drone_px4.drone_px4 import DronePx4


def apply_dance_size_check_procedure(
    drone_px4: DronePx4,
) -> Displayer:
    dance_size_check = Displayer("Dance size")
    if get_dance_size(drone_px4) < JSON_BINARY_PARAMETER.dance_size_max:
        dance_size_check.validate()
    return dance_size_check
