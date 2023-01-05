from ..report import Contenor
from .show_px4_check.show_px4_check_report import ShowPx4CheckReport
from .show_simulation_collision_check.show_simulation_collision_check_procedure import (
    ShowSimulationCollisionCheckReport,
)
from .show_trajectory_performance_check.show_trajectory_performance_check_report import (
    ShowTrajectoryPerformanceCheckReport,
)


class ShowCheckReport(Contenor):
    def __init__(
        self,
        show_px4_check_report: ShowPx4CheckReport,
        show_trajectory_performance_check_report: ShowTrajectoryPerformanceCheckReport,
        show_simulation_collision_check_report: ShowSimulationCollisionCheckReport,
    ):
        self.name = "Show Check Report"
        self.show_px4_check_report = show_px4_check_report
        self.show_trajectory_performance_check_report = (
            show_trajectory_performance_check_report
        )

        self.show_simulation_collision_check_report = (
            show_simulation_collision_check_report
        )

    def update(self) -> None:
        self.validation = (
            self.show_px4_check_report.validation
            and self.show_trajectory_performance_check_report.validation
            and self.show_simulation_collision_check_report.validation
        )
