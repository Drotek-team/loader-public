# pyright: reportIncompatibleMethodOverride=false
from typing import Optional

from loader.parameters import IostarPhysicParameters
from loader.schemas import DronePx4, Metadata, ShowUser

from .autopilot_format_report import AutopilotFormatReport, AutopilotFormatReportSummary
from .base import BaseReport, BaseReportSummary
from .collision_report import CollisionReport, CollisionReportSummary
from .dance_size_report import DanceSizeReport, DanceSizeReportSummary
from .performance_report import PerformanceReport, PerformanceReportSummary
from .takeoff_format_report import TakeoffFormatReport, TakeoffFormatReportSummary


class GlobalReportSummary(BaseReportSummary):
    takeoff_format_summary: Optional[TakeoffFormatReportSummary] = None
    autopilot_format_summary: Optional[AutopilotFormatReportSummary] = None
    dance_size_summary: Optional[DanceSizeReportSummary] = None
    performance_summary: Optional[PerformanceReportSummary] = None
    collision_summary: Optional[CollisionReportSummary] = None
    physical_parameters: Optional[IostarPhysicParameters] = None
    metadata: Metadata = Metadata()


class GlobalReport(BaseReport):
    takeoff_format: Optional[TakeoffFormatReport] = None
    autopilot_format: Optional[AutopilotFormatReport] = None
    dance_size: Optional[DanceSizeReport] = None
    performance: Optional[PerformanceReport] = None
    collision: Optional[CollisionReport] = None
    physical_parameters: Optional[IostarPhysicParameters] = None
    metadata: Metadata = Metadata()

    def summarize(self) -> GlobalReportSummary:
        return GlobalReportSummary(
            takeoff_format_summary=self.takeoff_format.summarize()
            if self.takeoff_format is not None
            else None,
            autopilot_format_summary=self.autopilot_format.summarize()
            if self.autopilot_format is not None
            else None,
            dance_size_summary=self.dance_size.summarize() if self.dance_size is not None else None,
            performance_summary=self.performance.summarize()
            if self.performance is not None
            else None,
            collision_summary=self.collision.summarize() if self.collision is not None else None,
            metadata=self.metadata,
        )

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
        *,
        without_takeoff_format: bool = False,
        is_partial: bool = False,
        is_import: bool = False,
    ) -> "GlobalReport":
        if without_takeoff_format:
            takeoff_format_report = None
        else:
            takeoff_format_report = TakeoffFormatReport.generate_or_none(show_user)
        autopilot_format = DronePx4.from_show_user(show_user)
        autopilot_format_report = AutopilotFormatReport.generate_or_none(autopilot_format)
        dance_size_report = DanceSizeReport.generate_or_none(autopilot_format)
        if (
            takeoff_format_report is not None
            or autopilot_format_report is not None
            or dance_size_report is not None
        ):
            return GlobalReport(
                takeoff_format=takeoff_format_report,
                autopilot_format=autopilot_format_report,
                dance_size=dance_size_report,
                metadata=show_user.metadata,
            )
        performance_report = PerformanceReport.generate_or_none(
            show_user,
            is_partial=is_partial,
            is_import=is_import,
        )
        collision_report = CollisionReport.generate_or_none(
            show_user,
            is_partial=is_partial,
        )
        return GlobalReport(
            performance=performance_report,
            collision=collision_report,
            metadata=show_user.metadata,
        )
