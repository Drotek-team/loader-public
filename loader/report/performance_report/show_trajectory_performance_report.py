from typing import List, Optional

from loader.parameter.iostar_physic_parameter import IostarPhysicParameter
from loader.report.base import BaseReport
from loader.show_env.migration_su_to_stp.su_to_stp import su_to_stp
from loader.show_env.show_user import ShowUser

from .performance_evaluation import (
    PerformanceInfraction,
)


class PerformanceReport(BaseReport):
    performance_infractions: List[PerformanceInfraction] = []

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
        *,
        physic_parameter: Optional[IostarPhysicParameter] = None,
    ) -> Optional["PerformanceReport"]:
        performance_infracions = PerformanceInfraction.generate(
            su_to_stp(show_user),
            physic_parameter=physic_parameter,
        )
        if performance_infracions:
            return PerformanceReport(performance_infractions=performance_infracions)
        return None
