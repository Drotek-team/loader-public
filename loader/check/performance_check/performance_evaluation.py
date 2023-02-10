import copy
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict, List

import numpy as np

from loader.check.performance_check.migration.show_trajectory_performance import (
    Performance,
)
from loader.parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from loader.parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from loader.report.report import BaseInfraction


@dataclass(frozen=True)
class MetricRange:
    threshold: float
    standard_convention: bool = True

    def validation(self, value: float) -> bool:
        if self.standard_convention:
            return value <= self.threshold
        return value >= self.threshold


class Metric(Enum):
    VERTICAL_POSITION = "vertical position"
    HORIZONTAL_VELOCITY = "horizontal velocity"
    UP_VELOCITY = "up velocity"
    DOWN_VELOCITY = "down velocity"
    ACCELERATION = "acceleration"

    @property
    def evaluation(self) -> Callable[[Performance], float]:
        return METRICS_EVALUATION[self]

    @property
    def range_(self) -> MetricRange:
        return METRICS_RANGE[self]

    def validation(self, performance: Performance) -> bool:
        return self.range_.validation(self.evaluation(performance))


def vertical_position_evaluation(performance: Performance) -> float:
    return float(performance.position[2])


def horizontal_velocity_evaluation(performance: Performance) -> float:
    return float(np.linalg.norm(performance.velocity[0:2]))


def up_velocity_evaluation(performance: Performance) -> float:
    return float(performance.velocity[2])


def down_velocity_evaluation(performance: Performance) -> float:
    return float(-performance.velocity[2])


def acceleration_evaluation(performance: Performance) -> float:
    return float(np.linalg.norm(performance.acceleration))


METRICS_EVALUATION: Dict[Metric, Callable[[Performance], float]] = {
    Metric.VERTICAL_POSITION: vertical_position_evaluation,
    Metric.HORIZONTAL_VELOCITY: horizontal_velocity_evaluation,
    Metric.UP_VELOCITY: up_velocity_evaluation,
    Metric.DOWN_VELOCITY: down_velocity_evaluation,
    Metric.ACCELERATION: acceleration_evaluation,
}


class MetricsRange(Dict[Metric, MetricRange]):
    def update(self, new_metric_range: Dict[Metric, MetricRange]) -> None:
        for metric in new_metric_range:
            self[metric] = new_metric_range[metric]


METRICS_RANGE = MetricsRange(
    {
        Metric.VERTICAL_POSITION: MetricRange(
            threshold=TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
            standard_convention=False,
        ),
        Metric.HORIZONTAL_VELOCITY: MetricRange(
            IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max,
        ),
        Metric.UP_VELOCITY: MetricRange(IOSTAR_PHYSIC_PARAMETER.velocity_up_max),
        Metric.DOWN_VELOCITY: MetricRange(IOSTAR_PHYSIC_PARAMETER.velocity_down_max),
        Metric.ACCELERATION: MetricRange(IOSTAR_PHYSIC_PARAMETER.acceleration_max),
    },
)

METRICS_RANGE_COPY = copy.copy(METRICS_RANGE)


class PerformanceInfraction(BaseInfraction):
    performance_name: str
    drone_index: int
    frame: int
    value: float
    threshold: float
    metric_convention: bool


def get_performance_infractions_from_performance(
    drone_index: int,
    frame: int,
    performance: Performance,
) -> List[PerformanceInfraction]:
    return [
        PerformanceInfraction(
            performance_name=metric.value,
            drone_index=drone_index,
            frame=frame,
            value=metric.evaluation(performance),
            threshold=metric.range_.threshold,
            metric_convention=metric.range_.standard_convention,
        )
        for metric in Metric
        if not metric.validation(performance)
    ]
