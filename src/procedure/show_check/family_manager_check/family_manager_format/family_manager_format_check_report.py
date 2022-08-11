from ....report import Contenor, Displayer
from typing import Tuple


class NbxFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return (
            f"The number of drone according to x (nb_x) does not have the right format"
        )


class NbyFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return (
            f"The number of drone according to y (nb_y) does not have the right format"
        )


class StepFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The step between drones (step) does not have the right format"


class TakeoffAngleFormatCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The takeoff angle does not have the right format"


class FamilyManagerFormatCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Format Check Report"
        self.nbx_format_check_report = NbxFormatCheckReport()
        self.nby_format_check_report = NbyFormatCheckReport()
        self.step_format_check_report = StepFormatCheckReport()
        self.takeoff_angle_format_check_report = TakeoffAngleFormatCheckReport()
