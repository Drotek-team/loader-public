from .report import Contenor
from .IJ_param_check.IJ_param_check_report import IostarJsonParameterCheckReport
from .drones_px4_check.dance_check_report import DanceSizeCheckReport
from .show_simulation_check.simulation_check_procedure import SimulationCheckReport
from .drones_px4_check.dance_check_report import DanceCheckReport
from .drones_simulation_check.drone_simulation_check_report import (
    DroneSimulationCheckReport,
)


class ShowCheckReport(Contenor):
    def __init__(self, nb_drones: int = 1):
        self.name = "Show Check Report"
        self.simulation_check_report = SimulationCheckReport()
        self.family_check_report = IostarJsonParameterCheckReport()
        self.drones_check_report = [
            DanceCheckReport(drone_index) for drone_index in range(nb_drones)
        ]
        self.drones_simulation_check_report = [
            DroneSimulationCheckReport(drone_index) for drone_index in range(nb_drones)
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
