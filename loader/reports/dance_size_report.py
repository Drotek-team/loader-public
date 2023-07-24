# pyright: reportIncompatibleMethodOverride=false
import struct
from typing import List, Optional, Union

from tqdm import tqdm

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.reports.base import (
    BaseInfraction,
    BaseInfractionsSummary,
    BaseReport,
    BaseReportSummary,
    apply_func_on_optional_pair,
)
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.show_user.show_user import ShowUser


class DanceSizeInfraction(BaseInfraction):
    drone_index: int
    dance_size: int
    position_percent: float
    color_percent: float
    fire_percent: float

    @property
    def total_percent(self) -> float:
        return self.position_percent + self.color_percent + self.fire_percent

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
            position_percent=round(100 * position_size / JSON_BINARY_PARAMETERS.dance_size_max, 2),
            color_percent=round(100 * color_size / JSON_BINARY_PARAMETERS.dance_size_max, 2),
            fire_percent=round(100 * fire_size / JSON_BINARY_PARAMETERS.dance_size_max, 2),
        )

    def __len__(self) -> int:
        return int(self.dance_size >= JSON_BINARY_PARAMETERS.dance_size_max)

    def summarize(self) -> "DanceSizeInfractionsSummary":
        return DanceSizeInfractionsSummary(
            nb_infractions=len(self),
            min_dance_size_infraction=self if len(self) else None,
            max_dance_size_infraction=self if len(self) else None,
        )


class DanceSizeInfractionsSummary(BaseInfractionsSummary):
    min_dance_size_infraction: Optional[DanceSizeInfraction] = None
    max_dance_size_infraction: Optional[DanceSizeInfraction] = None

    def __add__(self, other: "DanceSizeInfractionsSummary") -> "DanceSizeInfractionsSummary":
        return DanceSizeInfractionsSummary(
            nb_infractions=self.nb_infractions + other.nb_infractions,
            min_dance_size_infraction=apply_func_on_optional_pair(
                self.min_dance_size_infraction,
                other.min_dance_size_infraction,
                lambda x, y: x if x.dance_size < y.dance_size else y,
            ),
            max_dance_size_infraction=apply_func_on_optional_pair(
                self.max_dance_size_infraction,
                other.max_dance_size_infraction,
                lambda x, y: x if x.dance_size > y.dance_size else y,
            ),
        )


class DanceSizeReportSummary(BaseReportSummary):
    dance_size_infractions_summary: Optional[DanceSizeInfractionsSummary]


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

    def summarize(self) -> DanceSizeReportSummary:
        return DanceSizeReportSummary(
            dance_size_infractions_summary=sum(
                (
                    dance_size_infraction.summarize()
                    for dance_size_infraction in tqdm(
                        self.dance_size_infractions,
                        desc="Summarizing dance size report",
                        unit="dance size infraction",
                    )
                ),
                DanceSizeInfractionsSummary(),
            ),
        )
