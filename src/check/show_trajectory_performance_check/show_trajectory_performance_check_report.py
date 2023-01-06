from typing import List

from ...report import *

# class PerformanceInfraction(Displayer):
#     absolute_time: float
#     performance_name: str
#     performance_value: float
#     performance_value_min: float
#     performance_value_max: float

#     def get_report(self) -> str:
#         return f"The performance {self.performance_name} has the value: {self.performance_value} (min/max:{self.performance_value_min}/{self.performance_value_max}) at the time {self.absolute_time}"


class DronePerformanceCheckReport(Contenor):
    def __init__(self, name: str):
        self.name = name
        self.performance_infractions: List[Displayer] = []


class ShowTrajectoryPerformanceCheckReport(Contenor):
    def __init__(self, nb_drone: int):
        self.name = "Performance check report"
        self.drones_trajectory_performance_check_report = [
            DronePerformanceCheckReport(
                f"Drone {drone_index} Trajectory Performance check report"
            )
            for drone_index in range(nb_drone)
        ]

    def update(self) -> None:
        self.validation = all(
            drone_trajectory_performance_check_report.validation
            for drone_trajectory_performance_check_report in self.drones_trajectory_performance_check_report
        )
