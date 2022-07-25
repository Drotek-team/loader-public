from .json_conversion.json_creation_report import JsonCreationReport
from .report import Contenor
from .show_check.show_check_report import ShowCheckReport


class ExportReport(Contenor):
    name = "Export Report"

    def __init__(self):
        self.show_check_report = ShowCheckReport()
        self.json_creation_report = JsonCreationReport()

    def update(self) -> None:
        self.validation = (
            self.show_check_report.validation and self.json_creation_report.validation
        )
