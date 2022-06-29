from .drones_creation.drone_creation_report import DroneCreationReport
from .show_check.show_check_report import ShowCheckReport


class ImportReport:
    def __init__(self):
        self.drone_creation_report = DroneCreationReport()
        self.show_check_report = ShowCheckReport()
