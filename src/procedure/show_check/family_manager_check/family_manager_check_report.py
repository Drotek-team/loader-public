from ...report import Contenor
from .family_manager_format.family_manager_format_check_report import (
    FamilyUserFormatCheckReport,
)
from .family_manager_value_check.family_manager_value_check_report import (
    FamilyUserValueCheckReport,
)
from .family_manager_logic_check.family_manager_logic_check_report import (
    FamilyUserLogicCheckReport,
)


class FamilyUserCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Check Report"
        self.family_manager_format_check_report = FamilyUserFormatCheckReport()
        self.family_manager_value_check_report = FamilyUserValueCheckReport()
        self.family_manager_logic_check_report = FamilyUserLogicCheckReport()

    def update(self) -> None:
        self.validation = (
            self.family_manager_format_check_report.validation
            and self.family_manager_value_check_report.validation
            and self.family_manager_logic_check_report.validation
        )
