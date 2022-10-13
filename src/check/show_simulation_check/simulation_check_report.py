from ...report import Contenor
from .collision_check.collision_check_report import CollisionCheckReport
from typing import List


class SimulationCheckReport(Contenor):
    def __init__(self, frames: List[int]):
        self.name = "Simulation Check Report"
        self.collision_check_report = CollisionCheckReport(frames)

    def update(self) -> None:
        self.validation = self.collision_check_report.validation
