from dataclasses import dataclass
from typing import List

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True)
class Performance:
    position: npt.NDArray[np.float64]
    velocity: npt.NDArray[np.float64]
    acceleration: npt.NDArray[np.float64]


@dataclass(frozen=True)
class TrajectoryPerformanceInfo:
    frame: int
    performance: Performance

    @property
    def position(self) -> npt.NDArray[np.float64]:
        return self.performance.position

    @property
    def velocity(self) -> npt.NDArray[np.float64]:
        return self.performance.velocity

    @property
    def acceleration(self) -> npt.NDArray[np.float64]:
        return self.performance.acceleration


class DroneTrajectoryPerformance:
    def __init__(
        self,
        index: int,
        trajectory_performance_infos: List[TrajectoryPerformanceInfo],
    ):
        self.index = index
        self.trajectory_performance_infos = trajectory_performance_infos


class ShowTrajectoryPerformance:
    def __init__(self, drones_trajectory_performance: List[DroneTrajectoryPerformance]):
        self.drones_trajectory_performance = drones_trajectory_performance

    @property
    def nb_drones(self):
        return len(self.drones_trajectory_performance)
