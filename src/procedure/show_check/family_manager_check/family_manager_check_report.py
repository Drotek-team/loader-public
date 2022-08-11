from ...report import Contenor
from .family_manager_format.family_manager_format_check_report import (
    FamilyManagerFormatCheckReport,
)
from .family_manager_value_check.family_manager_value_check_report import (
    FamilyManagerValueCheckReport,
)
from .family_manager_logic_check.family_manager_logic_check_report import (
    FamilyManagerLogicCheckReport,
)


class FamilyManagerCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Check Report"
        self.family_manager_format_check_report = FamilyManagerFormatCheckReport()
        self.family_manager_value_check_report = FamilyManagerValueCheckReport()
        self.family_manager_logic_check_report = FamilyManagerLogicCheckReport()

    def update(self) -> None:
        self.validation = (
            self.family_manager_format_check_report.validation
            and self.family_manager_value_check_report.validation
            and self.family_manager_logic_check_report.validation
        )
