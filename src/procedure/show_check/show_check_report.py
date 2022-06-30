from .drone_check.drone_check_report import DroneCheckReport
from .family_manager_check.family_manager_check_report import FamilyManagerCheckReport
from .simulation_check.simulation_check_report import SimulationCheckReport


class ShowCheckReport:
    def __init__(self, nb_drones: int):
        self.validation = False
        self.simulation_check_report = SimulationCheckReport()
        self.family_check_report = FamilyManagerCheckReport()
        self.drones_check_report = [DroneCheckReport() for _ in range(nb_drones)]

    def update(self) -> None:
        self.validation = (
            self.simulation_check_report.validation
            and self.family_check_report.validation
            and all(
                drone_check_report.validation
                for drone_check_report in self.drones_check_report
            )
        )
