from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict

import numpy as np

from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from ...report import Contenor, PerformanceInfraction
from ..performance_check.migration.show_trajectory_performance import Performance


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
    def evaluation(self):
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
        for metric in self:
            self[metric] = new_metric_range[metric]


METRICS_RANGE = MetricsRange(
    {
        Metric.VERTICAL_POSITION: MetricRange(
            threshold=TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
            standard_convention=False,
        ),
        Metric.HORIZONTAL_VELOCITY: MetricRange(
            IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max
        ),
        Metric.UP_VELOCITY: MetricRange(IOSTAR_PHYSIC_PARAMETER.velocity_up_max),
        Metric.DOWN_VELOCITY: MetricRange(IOSTAR_PHYSIC_PARAMETER.velocity_down_max),
        Metric.ACCELERATION: MetricRange(IOSTAR_PHYSIC_PARAMETER.acceleration_max),
    }
)


def performance_evaluation(frame: int, performance: Performance) -> Contenor:
    performance_evaluation_contenor = Contenor(
        f"Performance evaluation at frame {frame}"
    )
    for metric in Metric:
        if metric.validation(performance):
            continue
        performance_evaluation_contenor.add_error_message(
            PerformanceInfraction(
                name=metric.value,
                frame=frame,
                value=metric.evaluation(performance),
                threshold=metric.range_.threshold,
                metric_convention=metric.range_.standard_convention,
            )
        )
    return performance_evaluation_contenor
