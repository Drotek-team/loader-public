import copy
import itertools
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List

import numpy as np

from loader.parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from loader.report.base import BaseInfraction
from loader.report.performance_report.migration.show_trajectory_performance import (
    Performance,
)

from .migration.show_trajectory_performance import (
    DroneTrajectoryPerformance,
    ShowTrajectoryPerformance,
)


@dataclass(frozen=True)
class PerformanceRange:
    threshold: float

    def validation(self, value: float) -> bool:
        return value <= self.threshold


class PerformanceKind(Enum):
    HORIZONTAL_VELOCITY = "horizontal velocity"
    UP_VELOCITY = "up velocity"
    DOWN_VELOCITY = "down velocity"
    ACCELERATION = "acceleration"

    @property
    def evaluation(self) -> Callable[[Performance], float]:
        return PERFORMANCES_EVALUATION[self]

    @property
    def range_(self) -> PerformanceRange:
        return PERFORMANCES_RANGE[self]

    def validation(self, performance: Performance) -> bool:
        return self.range_.validation(self.evaluation(performance))


def horizontal_velocity_evaluation(performance: Performance) -> float:
    return float(np.linalg.norm(performance.velocity[0:2]))


def up_velocity_evaluation(performance: Performance) -> float:
    return float(performance.velocity[2])


def down_velocity_evaluation(performance: Performance) -> float:
    return float(-performance.velocity[2])


def acceleration_evaluation(performance: Performance) -> float:
    return float(np.linalg.norm(performance.acceleration))


PERFORMANCES_EVALUATION: Dict[PerformanceKind, Callable[[Performance], float]] = {
    PerformanceKind.HORIZONTAL_VELOCITY: horizontal_velocity_evaluation,
    PerformanceKind.UP_VELOCITY: up_velocity_evaluation,
    PerformanceKind.DOWN_VELOCITY: down_velocity_evaluation,
    PerformanceKind.ACCELERATION: acceleration_evaluation,
}


class PerformancesRange(Dict[PerformanceKind, PerformanceRange]):
    def reset(self) -> None:
        for performance in self:
            self[performance] = PERFORMANCES_RANGE_COPY[performance]


PERFORMANCES_RANGE = PerformancesRange(
    {
        PerformanceKind.HORIZONTAL_VELOCITY: PerformanceRange(
            IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max,
        ),
        PerformanceKind.UP_VELOCITY: PerformanceRange(
            IOSTAR_PHYSIC_PARAMETER.velocity_up_max,
        ),
        PerformanceKind.DOWN_VELOCITY: PerformanceRange(
            IOSTAR_PHYSIC_PARAMETER.velocity_down_max,
        ),
        PerformanceKind.ACCELERATION: PerformanceRange(
            IOSTAR_PHYSIC_PARAMETER.acceleration_max,
        ),
    },
)

PERFORMANCES_RANGE_COPY = copy.copy(PERFORMANCES_RANGE)


class PerformanceInfraction(BaseInfraction):
    performance_name: str
    drone_index: int
    frame: int
    value: float
    threshold: float

    @classmethod
    def _get_performance_infractions_from_performance(
        cls,
        drone_index: int,
        frame: int,
        performance: Performance,
    ) -> List["PerformanceInfraction"]:
        return [
            PerformanceInfraction(
                performance_name=performance_kind.value,
                drone_index=drone_index,
                frame=frame,
                value=performance_kind.evaluation(performance),
                threshold=performance_kind.range_.threshold,
            )
            for performance_kind in PerformanceKind
            if not performance_kind.validation(performance)
        ]

    @classmethod
    def _get_performance_infractions_from_drone_performance(
        cls,
        drone_trajectory_performance: DroneTrajectoryPerformance,
    ) -> List["PerformanceInfraction"]:
        return list(
            itertools.chain.from_iterable(
                cls._get_performance_infractions_from_performance(
                    drone_trajectory_performance.index,
                    trajectory_performance_info.frame,
                    trajectory_performance_info.performance,
                )
                for (
                    trajectory_performance_info
                ) in drone_trajectory_performance.trajectory_performance_infos
            ),
        )

    @classmethod
    def generate(
        cls,
        show_trajectory_performance: ShowTrajectoryPerformance,
    ) -> List["PerformanceInfraction"]:
        return list(
            itertools.chain.from_iterable(
                cls._get_performance_infractions_from_drone_performance(
                    drone_trajectory_performance,
                )
                for (
                    drone_trajectory_performance
                ) in show_trajectory_performance.drones_trajectory_performance
            ),
        )
