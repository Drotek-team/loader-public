# pyright: reportIncompatibleMethodOverride=false
import itertools
from collections import defaultdict
from typing import DefaultDict, List, Optional, Set

from pydantic import Field, field_serializer
from tqdm import tqdm
from typing_extensions import Annotated

from loader.parameters import IostarPhysicParameters
from loader.reports.base import BaseReport, BaseReportSummary
from loader.reports.ranges import get_ranges_from_drone_indices
from loader.schemas.show_user import ShowUser

from .performance_infraction import PerformanceInfraction, PerformanceInfractionsSummary


class PerformanceReportSummary(BaseReportSummary):
    drone_indices: Set[int] = set()
    performance_infractions_summary: DefaultDict[
        str,
        Annotated[
            PerformanceInfractionsSummary,
            Field(default_factory=PerformanceInfractionsSummary),
        ],
    ] = defaultdict(
        PerformanceInfractionsSummary,
    )

    def __add__(self, other: "PerformanceReportSummary") -> "PerformanceReportSummary":
        return PerformanceReportSummary(
            drone_indices=self.drone_indices.union(other.drone_indices),
            performance_infractions_summary=defaultdict(
                PerformanceInfractionsSummary,
                {
                    key: self.performance_infractions_summary[key]
                    + other.performance_infractions_summary[key]
                    for key in set(
                        itertools.chain(
                            self.performance_infractions_summary.keys(),
                            other.performance_infractions_summary.keys(),
                        ),
                    )
                },
            ),
        )

    @field_serializer("drone_indices")
    def _serialize_drone_indices(self, value: Set[int]) -> str:
        return get_ranges_from_drone_indices(value)


class PerformanceReport(BaseReport):
    performance_infractions: List[PerformanceInfraction] = []

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
        *,
        physic_parameters: Optional[IostarPhysicParameters] = None,
        is_partial: bool = False,
    ) -> "PerformanceReport":
        performance_infracions = PerformanceInfraction.generate(
            show_user,
            physic_parameters=physic_parameters,
            is_partial=is_partial,
        )
        return PerformanceReport(performance_infractions=performance_infracions)

    def summarize(self) -> PerformanceReportSummary:
        return sum(
            (
                PerformanceReportSummary(
                    drone_indices={performance_infraction.drone_index},
                    performance_infractions_summary=defaultdict(
                        PerformanceInfractionsSummary,
                        {
                            performance_infraction.performance_name: performance_infraction.summarize(),
                        },
                    ),
                )
                for performance_infraction in tqdm(
                    self.performance_infractions,
                    desc="Summarizing performance report",
                    unit="performance infraction",
                )
            ),
            PerformanceReportSummary(
                performance_infractions_summary=defaultdict(PerformanceInfractionsSummary),
            ),
        )
