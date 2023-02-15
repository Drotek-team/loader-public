from typing import List, Optional

from loader.report.base import BaseReport
from loader.show_env.show_user import ShowUser

from .migration.su_to_stp import su_to_stp
from .performance_evaluation import (
    PerformanceInfraction,
)


class PerformanceReport(BaseReport):
    performance_infractions: List[PerformanceInfraction] = []

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
    ) -> Optional["PerformanceReport"]:
        performance_infracions = PerformanceInfraction.generate(
            su_to_stp(show_user),
        )
        if performance_infracions:
            return PerformanceReport(performance_infractions=performance_infracions)
        return None
