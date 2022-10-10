from ..report import Contenor
from .IJ_param_value_check.IJ_param_value_check_report import (
    FamilyUserValueCheckReport,
)
from .IJ_param_logic_check.IJ_param_logic_check_report import (
    FamilyUserLogicCheckReport,
)


class FamilyUserCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Check Report"
        self.family_user_value_check_report = FamilyUserValueCheckReport()
        self.family_user_logic_check_report = FamilyUserLogicCheckReport()

    def update(self) -> None:
        self.validation = (
            self.family_user_value_check_report.validation
            and self.family_user_logic_check_report.validation
        )
