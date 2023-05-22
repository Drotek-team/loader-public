# pyright: reportIncompatibleMethodOverride=false
from typing import Dict, Optional

from loader.reports.base import BaseReport
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.show_user import ShowUser

from .dances_size_report import DanceSizeReport
from .events_format_report import EventsFormatReport


class DronePx4Report(BaseReport):
    events_format_report: Optional[EventsFormatReport] = None
    dance_size_infraction: Optional[DanceSizeReport] = None

    @classmethod
    def generate(cls, drone_px4: DronePx4) -> "DronePx4Report":
        events_format_report = EventsFormatReport.generate_or_none(drone_px4)
        dance_size_infraction = DanceSizeReport.generate_or_none(drone_px4)
        return DronePx4Report(
            events_format_report=events_format_report,
            dance_size_infraction=dance_size_infraction,
        )


class AutopilotFormatReport(BaseReport):
    drone_px4_reports: Dict[int, DronePx4Report] = {}

    @classmethod
    def generate(cls, show_user: ShowUser) -> "AutopilotFormatReport":
        show_px4 = DronePx4.from_show_user(show_user)
        drone_px4_reports = {
            drone_px4.index: drone_px4_report
            for drone_px4 in show_px4
            if len(drone_px4_report := DronePx4Report.generate(drone_px4))
        }
        return AutopilotFormatReport(drone_px4_reports=drone_px4_reports)
