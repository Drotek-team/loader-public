from ..report import Contenor
from .show_simulation_check.simulation_check_procedure import SimulationCheckReport
from .show_px4_check.dance_check_report import DanceCheckReport
from .drones_dev_check.drone_dev_check_report import (
    DroneDevCheckReport,
)


class ShowCheckReport(Contenor):
    def __init__(self, nb_drones: int = 1):
        self.name = "Show Check Report"
        self.simulation_check_report = SimulationCheckReport()
        self.drones_check_report = [
            DanceCheckReport(drone_index) for drone_index in range(nb_drones)
        ]
        self.drones_dev_check_report = [
            DroneDevCheckReport(drone_index) for drone_index in range(nb_drones)
        ]

    def update(self) -> None:
        self.validation = self.simulation_check_report.validation and all(
            dance_check_report.validation
            for dance_check_report in self.drones_check_report
        )
