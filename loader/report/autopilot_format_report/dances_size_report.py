import struct
from typing import Optional

from pydantic import BaseModel

from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.report.base import BaseInfraction
from loader.show_env.drone_px4 import DronePx4


class DanceSizeInformation(BaseModel):
    drone_index: int
    dance_size: int
    position_events_size_pct: int
    color_events_size_pct: int
    fire_events_size_pct: int

    @property
    def total_events_size_pct(self) -> int:
        return (
            self.position_events_size_pct + self.color_events_size_pct + self.fire_events_size_pct
        )


def get_dance_size_information(drone_px4: DronePx4) -> DanceSizeInformation:
    header_size = struct.calcsize(JSON_BINARY_PARAMETER.fmt_header)
    header_section_size = len(drone_px4.non_empty_events_list) * struct.calcsize(
        JSON_BINARY_PARAMETER.fmt_section_header,
    )
    position_size = len(drone_px4.position_events) * struct.calcsize(
        JSON_BINARY_PARAMETER.position_event_format,
    )
    color_size = len(drone_px4.color_events) * struct.calcsize(
        JSON_BINARY_PARAMETER.color_event_format,
    )
    fire_size = len(drone_px4.fire_events) * struct.calcsize(
        JSON_BINARY_PARAMETER.fire_event_format,
    )
    return DanceSizeInformation(
        drone_index=drone_px4.index,
        dance_size=header_size + header_section_size + position_size + color_size + fire_size,
        position_events_size_pct=int(
            100 * position_size / JSON_BINARY_PARAMETER.dance_size_max,
        ),
        color_events_size_pct=int(
            100 * color_size / JSON_BINARY_PARAMETER.dance_size_max,
        ),
        fire_events_size_pct=int(
            100 * fire_size / JSON_BINARY_PARAMETER.dance_size_max,
        ),
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
