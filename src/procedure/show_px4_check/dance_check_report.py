from ..report import Contenor
from .dance_size_check.dances_size_check_report import DanceSizeCheckReport
from .events_format_check.events_format_check_report import EventsFormatCheckReport


class DanceCheckReport(Contenor):
    def __init__(self, drone_index: int):
        self.name = f"Dance {drone_index} check report"
        self.events_format_check_report = EventsFormatCheckReport()
        self.dance_size_check_report = DanceSizeCheckReport()

    def update(self) -> None:
        self.validation = (
            self.events_format_check_report.validation
            and self.dance_size_check_report.validation
        )
