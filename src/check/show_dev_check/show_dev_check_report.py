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


class DroneDevCheckReport(Contenor):
    def __init__(self, index: int):
        self.name = "Drone Simulation Check Report"
        self.index = index
        self.takeoff_check_report = TakeoffCheckReport()

    def update(self) -> None:
        self.validation = self.takeoff_check_report.validation


class ShowDevCheckReport(Contenor):
    def __init__(self, nb_drones: int):
        self.name = "Show dev Check Report"
        self.drones_dev_check_report = [
            DroneDevCheckReport(drone_index) for drone_index in range(nb_drones)
        ]

    def update(self) -> None:
        self.validation = all(
            drone_dev_check_report.validation
            for drone_dev_check_report in self.drones_dev_check_report
        )
