# pyright: reportIncompatibleMethodOverride=false
from typing import List, Optional

from loader.parameters import IostarPhysicParameters
from loader.reports.base import BaseReport
from loader.schemas.show_user import ShowUser

from .performance_infraction import PerformanceInfraction


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
