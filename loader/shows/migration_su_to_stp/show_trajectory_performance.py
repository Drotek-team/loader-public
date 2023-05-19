from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


@dataclass(frozen=True)
class Performance:
    position: NDArray[np.float64]
    velocity: NDArray[np.float64]
    acceleration: NDArray[np.float64]


@dataclass(frozen=True)
class TrajectoryPerformanceInfo:
    frame: int
    performance: Performance

    @property
    def position(self) -> NDArray[np.float64]:
        return self.performance.position

    @property
    def velocity(self) -> NDArray[np.float64]:
        return self.performance.velocity

    @property
    def acceleration(self) -> NDArray[np.float64]:
        return self.performance.acceleration


class DroneTrajectoryPerformance:
    def __init__(
        self,
        index: int,
        trajectory_performance_infos: list[TrajectoryPerformanceInfo],
    ) -> None:
        self.index = index
        self.trajectory_performance_infos = trajectory_performance_infos
