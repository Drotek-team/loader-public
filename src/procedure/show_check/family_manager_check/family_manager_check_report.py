from ...report import Contenor
from .family_manager_format.family_manager_format_check_report import (
    FamilyManagerFormatCheckReport,
)


class FamilyManagerCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Check Report"
        self.family_manager_format_check_report = FamilyManagerFormatCheckReport()
        self.family_manager_value_check_report = FamilyManagerValueCheckReport()
        self.coherence_check_report = CoherenceCheckReport()

    def update(self) -> None:
        self.validation = (
            self.family_manager_format_check_report.validation
            and self.family_manager_value_check_report.validation
            and self.coherence_check_report.validation
        )
