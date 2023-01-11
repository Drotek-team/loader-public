from report import Contenor

from .collision_check.show_simulation_collision_check_procedure import (
    ShowSimulationCollisionCheckReport,
)
from .performance_check.show_trajectory_performance_check_report import (
    ShowTrajectoryPerformanceCheckReport,
)
from .show_px4_check.show_px4_check_report import ShowPx4CheckReport
from .show_user_check.show_user_check_report import ShowUserCheckReport


class ShowCheckReport(Contenor):
    def __init__(self, nb_drones: int):
        self.name = "Show Check Report"
        self.show_user_check_report = ShowUserCheckReport(nb_drones)
        self.show_px4_check_report = ShowPx4CheckReport(nb_drones)
        self.show_trajectory_performance_check_report = (
            ShowTrajectoryPerformanceCheckReport(nb_drones)
        )
        self.show_simulation_collision_check_report = (
            ShowSimulationCollisionCheckReport()
        )
