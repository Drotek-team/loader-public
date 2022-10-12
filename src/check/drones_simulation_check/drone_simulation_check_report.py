from ...report import Displayer, Contenor


class TakeoffDurationCheckReport(Displayer):
    def get_report(self) -> str:
        return "Takeoff Duration Check Report"


class TakeoffPositionCheckReport(Displayer):
    def get_report(self) -> str:
        return "Takeoff Position Check Report"


class TakeoffCheckReport(Contenor):
    def __init__(self):
        self.name = "Takeoff Check Report"
        self.takeoff_duration_check_report = TakeoffDurationCheckReport()
        self.takeoff_xyz_check_report = TakeoffPositionCheckReport()

    def update(self):
        self.validation = (
            self.takeoff_duration_check_report.validation
            and self.takeoff_xyz_check_report.validation
        )


class DroneSimulationCheckReport(Contenor):
    def __init__(self, index: int):
        self.name = "Drone Simulation Check Report"
        self.index = index
        self.takeoff_check_report = TakeoffCheckReport()

    def update(self) -> None:
        self.validation = self.takeoff_check_report.validation
