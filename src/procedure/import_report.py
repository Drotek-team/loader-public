from .migration_IJ_DP.IJ_to_DP_report import JsonExtractionReport
from .report import Contenor
from .show_check_report import ShowCheckReport


class ImportReport(Contenor):
    def __init__(self):
        self.name = "Import Report"
        self.json_extraction_report = JsonExtractionReport()
        self.show_check_report = ShowCheckReport()

    def update(self) -> None:
        self.validation = self.json_extraction_report.validation
