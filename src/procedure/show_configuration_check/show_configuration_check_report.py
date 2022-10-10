from ..report import Contenor
from .show_configuration_value_check.show_configuration_value_check_report import (
    IostarJsonParameterValueCheckReport,
)
from .show_configuration_logic_check.show_configuration_logic_check_report import (
    IostarJsonParameterLogicCheckReport,
)


class IostarJsonParameterCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Check Report"
        self.show_configuration_value_check_report = (
            IostarJsonParameterValueCheckReport()
        )
        self.show_configuration_logic_check_report = (
            IostarJsonParameterLogicCheckReport()
        )

    def update(self) -> None:
        self.validation = (
            self.show_configuration_value_check_report.validation
            and self.show_configuration_logic_check_report.validation
        )
