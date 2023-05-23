# pyright: reportIncompatibleMethodOverride=false
from typing import List, Optional

from loader.reports.base import BaseReport
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.show_user import ShowUser

from .dance_size_report import DanceSizeReport
from .events_format_report import EventsFormatReport


class AutopilotFormatReport(BaseReport):
    events_format_reports: List[EventsFormatReport] = []
    dance_size_report: Optional[DanceSizeReport] = None

    @classmethod
    def generate(cls, show_user: ShowUser) -> "AutopilotFormatReport":
        show_px4 = DronePx4.from_show_user(show_user)
        events_format_reports = [
            events_format_report
            for drone_px4 in show_px4
            if len(events_format_report := EventsFormatReport.generate(drone_px4))
        ]
        dance_size_report = DanceSizeReport.generate_or_none(show_px4)
        return AutopilotFormatReport(
            events_format_reports=events_format_reports,
            dance_size_report=dance_size_report,
        )
