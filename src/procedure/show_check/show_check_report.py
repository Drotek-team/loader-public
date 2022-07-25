from ..report import Contenor
from .drone_check.dance_check_report import DanceCheckReport
from .family_manager_check.family_manager_check_report import FamilyManagerCheckReport
from .simulation_check.simulation_check_report import SimulationCheckReport


class ShowCheckReport(Contenor):
    def __init__(self):
        self.name = "Show Check Report"
        self.simulation_check_report = SimulationCheckReport()
        self.family_check_report = FamilyManagerCheckReport()

    def initialize_drones_check_report(self, nb_drones: int) -> None:
        self.drones_check_report = [
            DanceCheckReport(drone_index) for drone_index in range(nb_drones)
        ]

    def update(self) -> None:
        self.validation = (
            self.simulation_check_report.validation
            and self.family_check_report.validation
            and all(
                dance_check_report.validation
                for dance_check_report in self.drones_check_report
            )
        )
