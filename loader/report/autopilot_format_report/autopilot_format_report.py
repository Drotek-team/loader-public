from typing import Dict, Optional

from loader.report.base import BaseReport
from loader.show_env.autopilot_format.drone_px4 import DronePx4
from loader.show_env.migration_sp_su.su_to_sp import su_to_sp
from loader.show_env.show_user import ShowUser

from .dances_size_report import (
    DanceSizeInfraction,
    get_dance_size_infraction,
)
from .events_format_report import (
    EventsFormatReport,
)


class DronePx4Report(BaseReport):
    events_format_report: Optional[EventsFormatReport] = None
    dance_size_infraction: Optional[DanceSizeInfraction] = None

    @classmethod
    def generate(cls, drone_px4: DronePx4) -> Optional["DronePx4Report"]:
        events_format_report = EventsFormatReport.generate(
            drone_px4,
        )
        dance_size_infraction = get_dance_size_infraction(
            drone_px4,
        )
        if events_format_report is not None or dance_size_infraction is not None:
            return DronePx4Report(
                events_format_report=events_format_report,
                dance_size_infraction=dance_size_infraction,
            )
        return None


class AutopilotFormatReport(BaseReport):
    drone_px4_reports: Dict[int, DronePx4Report] = {}

    @classmethod
    def generate(cls, show_user: ShowUser) -> Optional["AutopilotFormatReport"]:
        show_px4 = su_to_sp(
            show_user,
        )
        drone_px4_reports = {
            drone_px4.index: drone_px4_report
            for drone_px4 in show_px4
            if (drone_px4_report := DronePx4Report.generate(drone_px4)) is not None
        }
        if drone_px4_reports:
            return AutopilotFormatReport(drone_px4_reports=drone_px4_reports)
        return None
