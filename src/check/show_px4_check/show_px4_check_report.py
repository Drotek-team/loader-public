from report import *

from .events_format_check.events_format_check_report import EventsFormatCheckReport


class DronePx4CheckReport(Contenor):
    def __init__(self, drone_index: int):
        self.name = f"Dance {drone_index} check report"
        self.events_format_check_report = EventsFormatCheckReport()
        self.dance_size_check_report = Displayer("Dance size Check Report")


class ShowPx4CheckReport(Contenor):
    def __init__(self, nb_drones: int):
        self.name = "Show px4 Check Report"
        self.drones_px4_check_report = [
            DronePx4CheckReport(drone_index) for drone_index in range(nb_drones)
        ]
