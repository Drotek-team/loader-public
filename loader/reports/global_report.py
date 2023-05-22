from typing import Optional

from pydantic import BaseModel, Extra

from loader.parameters import IostarPhysicParameters
from loader.schemas.show_user import ShowUser

from .autopilot_format_report import AutopilotFormatReport
from .base import BaseReport
from .collision_report import CollisionReport
from .performance_report import PerformanceReport
from .takeoff_format_report import TakeoffFormatReport


class GlobalReportSummary(BaseModel, extra=Extra.forbid):
    takeoff_format: int
    autopilot_format: int
    performance: int
    collision: int

    def is_valid(self) -> bool:
        return sum(getattr(self, field.name) for field in self.__fields__.values()) == 0


class GlobalReport(BaseReport):
    takeoff_format: Optional[TakeoffFormatReport] = None
    autopilot_format: Optional[AutopilotFormatReport] = None
    performance: Optional[PerformanceReport] = None
    collision: Optional[CollisionReport] = None

    def summary(self) -> GlobalReportSummary:
        return GlobalReportSummary(
            takeoff_format=self.takeoff_format.get_nb_errors() if self.takeoff_format else 0,
            autopilot_format=self.autopilot_format.get_nb_errors() if self.autopilot_format else 0,
            performance=self.performance.get_nb_errors() if self.performance else 0,
            collision=self.collision.get_nb_errors() if self.collision else 0,
        )

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
        *,
        without_takeoff_format: bool = False,
        physic_parameters: Optional["IostarPhysicParameters"] = None,
        is_partial: bool = False,
    ) -> "GlobalReport":
        if without_takeoff_format:
            takeoff_format_report = None
        else:
            takeoff_format_report = TakeoffFormatReport.generate_or_none(show_user)
        autopilot_format_report = AutopilotFormatReport.generate_or_none(show_user)
        if takeoff_format_report is not None or autopilot_format_report is not None:
            return GlobalReport(
                takeoff_format=takeoff_format_report,
                autopilot_format=autopilot_format_report,
            )
        performance_report = PerformanceReport.generate_or_none(
            show_user,
            physic_parameters=physic_parameters,
        )
        collision_report = CollisionReport.generate_or_none(
            show_user,
            physic_parameters=physic_parameters,
            is_partial=is_partial,
        )
        return GlobalReport(
            performance=performance_report,
            collision=collision_report,
        )
