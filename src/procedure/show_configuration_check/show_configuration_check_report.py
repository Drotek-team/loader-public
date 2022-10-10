from ..report import Contenor
from .show_configuration_value_check.show_configuration_value_check_report import (
    ShowConfigurationValueCheckReport,
)
from .show_configuration_logic_check.show_configuration_logic_check_report import (
    ShowConfigurationLogicCheckReport,
)


class ShowConfigurationCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Check Report"
        self.show_configuration_value_check_report = ShowConfigurationValueCheckReport()
        self.show_configuration_logic_check_report = ShowConfigurationLogicCheckReport()

    def update(self) -> None:
        self.validation = (
            self.show_configuration_value_check_report.validation
            and self.show_configuration_logic_check_report.validation
        )
