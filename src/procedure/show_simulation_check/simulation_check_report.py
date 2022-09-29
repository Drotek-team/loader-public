from ..report import Contenor
from .collision_check.collision_check_report import CollisionCheckReport
from .performance_check.performance_check_report import PerformanceCheckReport


class SimulationCheckReport(Contenor):
    def __init__(self):
        self.name = "Simulation Check Report"
        self.performance_check_report = PerformanceCheckReport()
        self.collision_check_report = CollisionCheckReport()

    def update(self) -> None:
        self.validation = (
            self.performance_check_report.validation
            and self.collision_check_report.validation
        )
