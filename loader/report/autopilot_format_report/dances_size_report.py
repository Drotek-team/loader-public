from typing import Optional

from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.report.base import BaseInfraction
from loader.show_env.autopilot_format.drone_px4 import DronePx4
from loader.show_env.migration_dp_binary.drone_encoding import (
    DanceSizeInformation,
    get_dance_size_information,
)


class DanceSizeInfraction(BaseInfraction, DanceSizeInformation):
    @classmethod
    def generate(
        cls,
        drone_px4: DronePx4,
    ) -> Optional["DanceSizeInfraction"]:
        dance_size_info = get_dance_size_information(drone_px4)
        if dance_size_info.dance_size >= JSON_BINARY_PARAMETER.dance_size_max:
            return DanceSizeInfraction.parse_obj(dance_size_info)
        return None
