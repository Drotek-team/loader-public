from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict

import numpy as np

from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from .show_trajectory_performance_check_report import *


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
    def range(self):
        return METRICS_RANGE[self]

    def validation(
        self, position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray
    ) -> bool:
        return self.range.validation(self.evaluation(position, velocity, acceleration))


def vertical_position_evaluation(
    position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray
) -> float:
    return float(position[2])


def horizontal_velocity_evaluation(
    position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray
) -> float:
    return float(np.linalg.norm(velocity[0:2]))


def up_velocity_evaluation(
    position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray
) -> float:
    return float(velocity[2])


def down_velocity_evaluation(
    position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray
) -> float:
    return float(-velocity[2])


def acceleration_evaluation(
    position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray
) -> float:
    return float(np.linalg.norm(acceleration))


METRICS_EVALUATION: Dict[
    Metric, Callable[[np.ndarray, np.ndarray, np.ndarray], float]
] = {
    Metric.VERTICAL_POSITION: vertical_position_evaluation,
    Metric.HORIZONTAL_VELOCITY: horizontal_velocity_evaluation,
    Metric.UP_VELOCITY: up_velocity_evaluation,
    Metric.DOWN_VELOCITY: down_velocity_evaluation,
    Metric.ACCELERATION: acceleration_evaluation,
}


@dataclass(frozen=True)
class MetricRange:
    threshold: float
    standard_convention: bool = True

    def validation(self, value: float) -> bool:
        if self.standard_convention:
            return value <= self.threshold
        return value >= self.threshold


METRICS_RANGE: Dict[Metric, MetricRange] = {
    Metric.VERTICAL_POSITION: MetricRange(
        TAKEOFF_PARAMETER.takeoff_altitude_meter_min, False
    ),
    Metric.HORIZONTAL_VELOCITY: MetricRange(
        IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max
    ),
    Metric.UP_VELOCITY: MetricRange(IOSTAR_PHYSIC_PARAMETER.velocity_up_max),
    Metric.DOWN_VELOCITY: MetricRange(IOSTAR_PHYSIC_PARAMETER.velocity_down_max),
    Metric.ACCELERATION: MetricRange(IOSTAR_PHYSIC_PARAMETER.acceleration_max),
}


def get_performance_infraction(
    performance_name: str,
    performance_value: float,
    metric_range: MetricRange,
    absolute_frame: int,
) -> Displayer:
    metric_convention_name = "max" if metric_range.standard_convention else "min"
    return Displayer(
        name=f"The performance {performance_name} has the value: {performance_value:.2f} ({metric_convention_name}: {metric_range.threshold}) at the frame {absolute_frame}",
        validation=False,
    )


def performance_evaluation(
    absolute_frame: int,
    position: np.ndarray,
    velocity: np.ndarray,
    acceleration: np.ndarray,
    drone_trajectory_performance_check: DronePerformanceCheckReport,
) -> None:
    for metric in Metric:
        if not (metric.validation(position, velocity, acceleration)):
            drone_trajectory_performance_check.performance_infractions.append(
                get_performance_infraction(
                    metric.value,
                    metric.evaluation(position, velocity, acceleration),
                    metric.range,
                    absolute_frame,
                )
            )
