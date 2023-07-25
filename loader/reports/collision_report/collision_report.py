# pyright: reportIncompatibleMethodOverride=false
from typing import List, Optional

from tqdm import tqdm

from loader.parameters import IostarPhysicParameters
from loader.reports.base import BaseReport, BaseReportSummary
from loader.schemas.show_user import ShowUser

from .collision_infraction import CollisionInfraction, CollisionInfractionsSummary


class CollisionReportSummary(BaseReportSummary):
    collision_infractions_summary: Optional["CollisionInfractionsSummary"] = None


class CollisionReport(BaseReport):
    collision_infractions: List[CollisionInfraction] = []

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
        *,
        physic_parameters: Optional[IostarPhysicParameters] = None,
        is_partial: bool = False,
    ) -> "CollisionReport":
        collision_infractions = CollisionInfraction.generate(
            show_user,
            collision_distance=(physic_parameters.minimum_distance if physic_parameters else None),
            is_partial=is_partial,
        )
        return CollisionReport(collision_infractions=collision_infractions)

    def summarize(self) -> CollisionReportSummary:
        return CollisionReportSummary(
            collision_infractions_summary=sum(
                (
                    collision_infraction.summarize()
                    for collision_infraction in tqdm(
                        self.collision_infractions,
                        desc="Summarizing collision report",
                        unit="collision",
                    )
                ),
                CollisionInfractionsSummary(),
            ),
        )
