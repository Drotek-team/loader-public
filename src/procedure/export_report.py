from .report import Contenor
from .show_check_report import ShowCheckReport


class ExportReport(Contenor):
    name = "Export Report"

    def __init__(self):
        self.show_check_report = ShowCheckReport()

    def update(self) -> None:
        self.validation = self.show_check_report.validation
