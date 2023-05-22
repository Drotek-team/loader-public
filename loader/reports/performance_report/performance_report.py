from typing import List, Optional

from loader.parameters import IostarPhysicParameters
from loader.reports.base import BaseReport
from loader.shows.show_user import ShowUser

from .performance_infraction import PerformanceInfraction


class PerformanceReport(BaseReport):
    performance_infractions: List[PerformanceInfraction] = []

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
        *,
        physic_parameters: Optional[IostarPhysicParameters] = None,
    ) -> Optional["PerformanceReport"]:
        performance_infracions = PerformanceInfraction.generate(
            show_user,
            physic_parameters=physic_parameters,
        )
        if performance_infracions:
            return PerformanceReport(performance_infractions=performance_infracions)
        return None
