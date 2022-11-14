from dataclasses import dataclass
from typing import List

from ...report import Contenor, Displayer


@dataclass(frozen=True)
class PerformanceInfraction(Displayer):
    absolute_frame: int
    performance_name: str
    performance_value: float
    performance_value_min: float
    performance_value_max: float

    def get_report(self) -> str:
        return f"The performance {self.performance_name} has the value: {self.performance_value} (min/max:{self.performance_value_min}/{self.performance_value_max}) at the position frame {self.absolute_frame}"


class DroneTrajectoryPerformanceCheckReport(Contenor):
    def __init__(self, drone_index: int):
        self.drone_index = drone_index
        self.name = f"Drone {drone_index} Trajectory Performance check report"
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
