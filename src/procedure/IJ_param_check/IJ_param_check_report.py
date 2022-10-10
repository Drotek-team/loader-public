from ..report import Contenor
from .IJ_param_value_check.IJ_param_value_check_report import (
    IostarJsonParameterValueCheckReport,
)
from .IJ_param_logic_check.IJ_param_logic_check_report import (
    IostarJsonParameterLogicCheckReport,
)


class IostarJsonParameterCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Check Report"
        self.iostar_json_parameter_value_check_report = (
            IostarJsonParameterValueCheckReport()
        )
        self.iostar_json_parameter_logic_check_report = (
            IostarJsonParameterLogicCheckReport()
        )

    def update(self) -> None:
        self.validation = (
            self.iostar_json_parameter_value_check_report.validation
            and self.iostar_json_parameter_logic_check_report.validation
        )
