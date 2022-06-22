from .drones_creation_report.drones_creation_report import DronesCreationReport
from .show_report.show_report import ShowReport


class ImportReport:
    def __init__(self):
        self.show_report = ShowReport()
        self.drones_creation_report = DronesCreationReport()
