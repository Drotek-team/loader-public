from .json_creation.json_creation_report import JsonCreationReport
from .show_check.show_check_report import ShowCheckReport


class ExportReport:
    def __init__(self):
        self.show_check_report = ShowCheckReport()
        self.json_creation_report = JsonCreationReport()
