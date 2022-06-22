from .dance_size_check.dances_size_check_report import ShowSizeCheckReport
from .events_format_check.events_format_check_report import EventsFormatCheckReport


class DroneCheckReport:
    def __init__(self):
        self.events_format_check_report = EventsFormatCheckReport()
        self.dance_size_check_report = ShowSizeCheckReport()
