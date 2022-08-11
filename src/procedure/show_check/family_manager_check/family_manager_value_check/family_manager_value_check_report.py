from ....report import Contenor, Displayer


class NbxValueCheckReport(Displayer):
    def get_report(self) -> str:
        return (
            f"The number of drone according to x (nb_x) does not have the right value"
        )


class NbyValueCheckReport(Displayer):
    def get_report(self) -> str:
        return (
            f"The number of drone according to y (nb_y) does not have the right value"
        )


class StepValueCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The step between drones (step) does not have the right value"


class TakeoffAngleValueCheckReport(Displayer):
    def get_report(self) -> str:
        return f"The takeoff angle does not have the right value"


class FamilyManagerValueCheckReport(Contenor):
    def __init__(self):
        self.name = "Family Manager Value Check Report"
        self.nbx_value_check_report = NbxValueCheckReport()
        self.nby_value_check_report = NbyValueCheckReport()
        self.step_value_check_report = StepValueCheckReport()
        self.takeoff_angle_value_check_report = TakeoffAngleValueCheckReport()
