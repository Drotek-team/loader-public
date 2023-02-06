from dataclasses import dataclass
from typing import Any, List


@dataclass(frozen=True)
class Performance:
    position: Any
    velocity: Any
    acceleration: Any


@dataclass(frozen=True)
class TrajectoryPerformanceInfo:
    frame: int
    performance: Performance

    @property
    def position(self) -> Any:
        return self.performance.position

    @property
    def velocity(self) -> Any:
        return self.performance.velocity

    @property
    def acceleration(self) -> Any:
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
