# pyright: reportIncompatibleMethodOverride=false
import struct
from typing import List, Union

from tqdm import tqdm

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.reports.base import BaseInfraction, BaseReport
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.show_user.show_user import ShowUser


class DanceSizeInfraction(BaseInfraction):
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

    @classmethod
    def generate(
        cls,
        drone_px4: DronePx4,
    ) -> "DanceSizeInfraction":
        header_size = struct.calcsize(JSON_BINARY_PARAMETERS.fmt_header)
        header_section_size = len(drone_px4.non_empty_events_list) * struct.calcsize(
            JSON_BINARY_PARAMETERS.fmt_section_header,
        )
        position_size = len(drone_px4.position_events) * struct.calcsize(
            JSON_BINARY_PARAMETERS.position_event_format,
        )
        color_size = len(drone_px4.color_events) * struct.calcsize(
            JSON_BINARY_PARAMETERS.color_event_format,
        )
        fire_size = len(drone_px4.fire_events) * struct.calcsize(
            JSON_BINARY_PARAMETERS.fire_event_format,
        )
        dance_size = header_size + header_section_size + position_size + color_size + fire_size

        return DanceSizeInfraction(
            drone_index=drone_px4.index,
            dance_size=dance_size,
            position_events_size_pct=round(
                100 * position_size / JSON_BINARY_PARAMETERS.dance_size_max,
            ),
            color_events_size_pct=round(
                100 * color_size / JSON_BINARY_PARAMETERS.dance_size_max,
            ),
            fire_events_size_pct=round(
                100 * fire_size / JSON_BINARY_PARAMETERS.dance_size_max,
            ),
        )

    def __len__(self) -> int:
        return int(self.dance_size >= JSON_BINARY_PARAMETERS.dance_size_max)


class DanceSizeReport(BaseReport):
    dance_size_infractions: List[DanceSizeInfraction] = []

    @classmethod
    def generate(
        cls,
        show_user_or_autopilot_format: Union[ShowUser, List[DronePx4]],
    ) -> "DanceSizeReport":
        if isinstance(show_user_or_autopilot_format, ShowUser):
            autopilot_format = DronePx4.from_show_user(show_user_or_autopilot_format)
        else:
            autopilot_format = show_user_or_autopilot_format

        dance_size_infractions = [
            DanceSizeInfraction.generate(drone_px4)
            for drone_px4 in tqdm(autopilot_format, desc="Checking dance size", unit="drone")
        ]
        return DanceSizeReport(dance_size_infractions=dance_size_infractions)
