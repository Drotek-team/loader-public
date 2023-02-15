from typing import Optional

from pydantic import BaseModel, Extra

from loader.show_env.show_user import ShowUser

from .base import BaseReport
from .collision_check.show_position_frames_collision_check import (
    CollisionReport,
    get_collision_report,
)
from .performance_check.show_trajectory_performance_check import (
    PerformanceReport,
    get_performance_report,
)
from .show_px4_check import ShowPx4Report
from .show_user_check import ShowUserReport


class GlobalReportSummary(BaseModel, extra=Extra.forbid):
    show_user: int
    show_px4: int
    performance: int
    collision: int

    def is_valid(self) -> bool:
        return sum(getattr(self, field.name) for field in self.__fields__.values()) == 0


class GlobalReport(BaseReport):
    show_user: Optional[ShowUserReport] = None
    show_px4: Optional[ShowPx4Report] = None
    performance: Optional[PerformanceReport] = None
    collision: Optional[CollisionReport] = None

    def summary(self) -> GlobalReportSummary:
        return GlobalReportSummary(
            show_user=self.show_user.get_nb_errors() if self.show_user else 0,
            show_px4=self.show_px4.get_nb_errors() if self.show_px4 else 0,
            performance=self.performance.get_nb_errors() if self.performance else 0,
            collision=self.collision.get_nb_errors() if self.collision else 0,
        )

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
    ) -> "GlobalReport":
        show_user_report = ShowUserReport.generate(show_user)
        show_px4_report = ShowPx4Report.generate(show_user)
        if show_user_report is not None or show_px4_report is not None:
            return GlobalReport(show_user=show_user_report, show_px4=show_px4_report)
        performance_report = get_performance_report(
            show_user,
        )
        collision_report = get_collision_report(
            show_user,
        )
        return GlobalReport(
            performance=performance_report,
            collision=collision_report,
        )
