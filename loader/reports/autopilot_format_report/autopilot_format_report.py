# pyright: reportIncompatibleMethodOverride=false
from typing import List, Union

from tqdm import tqdm

from loader.reports.base import BaseReport
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.show_user import ShowUser

from .events_format_report import EventsFormatReport


class AutopilotFormatReport(BaseReport):
    events_format_reports: List[EventsFormatReport] = []

    @classmethod
    def generate(
        cls,
        show_user_or_autopilot_format: Union[ShowUser, List[DronePx4]],
    ) -> "AutopilotFormatReport":
        if isinstance(show_user_or_autopilot_format, ShowUser):
            autopilot_format = DronePx4.from_show_user(show_user_or_autopilot_format)
        else:
            autopilot_format = show_user_or_autopilot_format

        events_format_reports = [
            events_format_report
            for drone_px4 in tqdm(autopilot_format, desc="Checking autopilot format", unit="drone")
            if len(events_format_report := EventsFormatReport.generate(drone_px4))
        ]
        return AutopilotFormatReport(
            events_format_reports=events_format_reports,
        )
