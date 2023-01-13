from typing import List

from ...report import *


class DronePerformanceCheckReport(Contenor):
    def __init__(self, drone_index: int):
        self.name = f"Performance drone {drone_index} check report"
        self.performance_infractions: List[Displayer] = []


class ShowTrajectoryPerformanceCheckReport(Contenor):
    def __init__(self, nb_drone: int):
        self.name = "Performance check report"
        self.drones_trajectory_performance_check_report = [
            DronePerformanceCheckReport(drone_index) for drone_index in range(nb_drone)
        ]
