from .collision_check.collision_check_report import CollisionCheckReport
from .performance_check.performance_check_report import PerformanceCheckReport


class SimulationCheckReport:
    def __init__(self):
        self.validate = True
        self.collision_check_report = PerformanceCheckReport()
        self.performance_check_report = CollisionCheckReport()
