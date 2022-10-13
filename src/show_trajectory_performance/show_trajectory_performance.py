from typing import List
import numpy as np
from dataclasses import dataclass


@dataclass(frozen=True)
class TrajectoryPerformanceInfo:
    position: np.ndarray
    velocity: np.ndarray
    acceleration: np.ndarray


class DroneTrajectoryPerformance:
    def __init__(
        self,
        drone_index: int,
        trajectory_performance_infos: List[TrajectoryPerformanceInfo],
    ):
        self.drone_index = drone_index
        self.trajectory_performance_infos = trajectory_performance_infos


class ShowTrajectoryPerformance:
    def __init__(self, drones_trajectory_performance: List[DroneTrajectoryPerformance]):
        self.drones_trajectory_performance = drones_trajectory_performance

    @property
    def nb_drones(self):
        return len(self.drones_trajectory_performance)
