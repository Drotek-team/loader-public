from typing import Optional

from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.report.report import BaseInfraction
from loader.show_env.migration_dp_binary.drone_encoding import get_dance_size
from loader.show_env.show_px4.drone_px4.drone_px4 import DronePx4


class DanceSizeInfraction(BaseInfraction):
    drone_index: int
    dance_size: int
    dance_size_max: int


def get_dance_size_infraction(
    drone_px4: DronePx4,
) -> Optional[DanceSizeInfraction]:
    if get_dance_size(drone_px4) >= JSON_BINARY_PARAMETER.dance_size_max:
        return DanceSizeInfraction(
            drone_index=drone_px4.index,
            dance_size=get_dance_size(drone_px4),
            dance_size_max=JSON_BINARY_PARAMETER.dance_size_max,
        )
    return None
