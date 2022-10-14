from ...report import Contenor, Displayer
from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PerformanceInfraction(Displayer):
    performance_name: str
    performance_value: float

    def get_report(self) -> str:
        return f"The performance {self.performance_name} has the value: {self.performance_value}"


class DroneTrajectoryPerformanceCheckReport(Contenor):
    def __init__(self, drone_index: int):
        self.drone_index = drone_index
        self.name = f"Drone Trajectory Performance check report"
        self.performance_infractions: List[PerformanceInfraction] = []

    def update(self) -> None:
        self.validation = not (self.performance_infractions)


class ShowTrajectoryPerformanceCheckReport(Contenor):
    def __init__(self, nb_drone: int):
        self.name = "Performance check report"
        self.drones_trajectory_performance_check_report = [
            DroneTrajectoryPerformanceCheckReport(drone_index)
            for drone_index in range(nb_drone)
        ]

    def update(self) -> None:
        self.validation = all(
            drone_trajectory_performance_check_report.validation
            for drone_trajectory_performance_check_report in self.drones_trajectory_performance_check_report
        )
