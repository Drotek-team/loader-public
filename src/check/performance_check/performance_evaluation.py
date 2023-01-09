from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict

import numpy as np

from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from .show_trajectory_performance_check_report import *


@dataclass(frozen=True)
class MetricRange:
    min_value: float
    max_value: float
    standard_convention: bool = True

    def interpolation(self, value: float) -> float:
        ratio = (value - self.min_value) / (self.max_value - self.min_value)
        return min(1, max(ratio, 0))

    def validation(self, value: float) -> bool:
        ratio = self.interpolation(value)
        return ratio != int(self.standard_convention)


def vertical_position_evaluation(
    position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray
) -> float:
    return float(position[2])


def horizontal_velocity_evaluation(
    position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray
) -> float:
    return float(np.linalg.norm(velocity[0:2]))


def horizontal_acceleration_evaluation(
    position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray
) -> float:
    return float(np.linalg.norm(acceleration[0:2]))


def up_velocity_evaluation(
    position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray
) -> float:
    return float(velocity[2])


def down_velocity_evaluation(
    position: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray
) -> float:
    return float(-velocity[2])


class Metric(Enum):
    VERTICAL_POSITION = "Vertical position"
    HORIZONTAL_VELOCITY = "horizontal velocity"
    HORIZONTAL_ACCELERATION = "horizontal acceleration"
    UP_VELOCITY = "up velocity"
    DOWN_VELOCITY = "donw velocity"


METRICS_EVALUATION: Dict[
    Metric, Callable[[np.ndarray, np.ndarray, np.ndarray], float]
] = {
    Metric.VERTICAL_POSITION: vertical_position_evaluation,
    Metric.HORIZONTAL_VELOCITY: horizontal_velocity_evaluation,
    Metric.HORIZONTAL_ACCELERATION: horizontal_acceleration_evaluation,
    Metric.UP_VELOCITY: up_velocity_evaluation,
    Metric.DOWN_VELOCITY: down_velocity_evaluation,
}


METRICS_RANGE: Dict[Metric, MetricRange] = {
    Metric.VERTICAL_POSITION: MetricRange(
        0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min, False
    ),
    Metric.HORIZONTAL_VELOCITY: MetricRange(
        0, IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max
    ),
    Metric.HORIZONTAL_ACCELERATION: MetricRange(
        0, IOSTAR_PHYSIC_PARAMETER.horizontal_acceleration_max
    ),
    Metric.UP_VELOCITY: MetricRange(0, IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max),
    Metric.DOWN_VELOCITY: MetricRange(
        IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max, 0, False
    ),
}


def performance_evaluation(
    absolute_time: float,
    position: np.ndarray,
    velocity: np.ndarray,
    acceleration: np.ndarray,
    drone_trajectory_performance_check: Displayer,
) -> None:
    for metric in Metric:
        if not (
            METRICS_RANGE[metric].validation(
                METRICS_EVALUATION[metric](position, velocity, acceleration)
            )
        ):
            drone_trajectory_performance_check.update_displayer(
                absolute_time,
                metric.value,
                METRICS_EVALUATION[metric](position, velocity, acceleration),
                METRICS_RANGE[metric].min_value,
                METRICS_RANGE[metric].max_value,
            )
