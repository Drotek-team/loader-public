from ..report import Contenor
from .show_simulation_check.simulation_check_procedure import SimulationCheckReport
from .show_px4_check.show_px4_check_report import ShowPx4CheckReport
from .show_dev_check.show_dev_check_report import (
    ShowDevCheckReport,
)


class ShowCheckReport(Contenor):
    def __init__(self, nb_drones):
        self.name = "Show Check Report"
        self.simulation_check_report = SimulationCheckReport(nb_drones)
        self.show_px4_check_report = ShowPx4CheckReport(nb_drones)
        self.show_dev_check_report = ShowDevCheckReport(nb_drones)

    def update(self) -> None:
        self.validation = (
            self.simulation_check_report.validation
            and self.show_px4_check_report.validation
            and self.show_dev_check_report.validation
        )
