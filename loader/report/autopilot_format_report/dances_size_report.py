from typing import Optional

from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.report.base import BaseInfraction
from loader.show_env.autopilot_format.drone_px4 import DronePx4
from loader.show_env.migration_dp_binary.drone_encoding import get_dance_size


class DanceSizeInfraction(BaseInfraction):
    drone_index: int
    dance_size: int
    dance_size_max: int

    @classmethod
    def generate(
        cls,
        drone_px4: DronePx4,
    ) -> Optional["DanceSizeInfraction"]:
        if get_dance_size(drone_px4) >= JSON_BINARY_PARAMETER.dance_size_max:
            return DanceSizeInfraction(
                drone_index=drone_px4.index,
                dance_size=get_dance_size(drone_px4),
                dance_size_max=JSON_BINARY_PARAMETER.dance_size_max,
            )
        return None
