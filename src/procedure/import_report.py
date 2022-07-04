from .json_extraction.json_extraction_report import JsonExtractionReport
from .show_check.show_check_report import ShowCheckReport


class ImportReport:
    def __init__(self):
        self.validation = False
        self.json_extraction_report = JsonExtractionReport()
        self.show_check_report = ShowCheckReport()

    def update(self) -> None:
        self.validation = (
            self.json_extraction_report.validation and self.show_check_report.validation
        )
