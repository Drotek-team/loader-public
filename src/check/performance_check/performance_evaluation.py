from dataclasses import dataclass
from enum import Enum
from typing import Callable, Dict

import numpy as np
import numpy.typing as npt

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
    def range_(self):
        return METRICS_RANGE[self]

    def validation(
        self,
        position: npt.NDArray[np.float64],
        velocity: npt.NDArray[np.float64],
        acceleration: npt.NDArray[np.float64],
    ) -> bool:
        return self.range_.validation(self.evaluation(position, velocity, acceleration))


def vertical_position_evaluation(
    position: npt.NDArray[np.float64],
    velocity: npt.NDArray[np.float64],
    acceleration: npt.NDArray[np.float64],
) -> float:
    return float(position[2])


def horizontal_velocity_evaluation(
    position: npt.NDArray[np.float64],
    velocity: npt.NDArray[np.float64],
    acceleration: npt.NDArray[np.float64],
) -> float:
    return float(np.linalg.norm(velocity[0:2]))


def up_velocity_evaluation(
    position: npt.NDArray[np.float64],
    velocity: npt.NDArray[np.float64],
    acceleration: npt.NDArray[np.float64],
) -> float:
    return float(velocity[2])


def down_velocity_evaluation(
    position: npt.NDArray[np.float64],
    velocity: npt.NDArray[np.float64],
    acceleration: npt.NDArray[np.float64],
) -> float:
    return float(-velocity[2])


def acceleration_evaluation(
    position: npt.NDArray[np.float64],
    velocity: npt.NDArray[np.float64],
    acceleration: npt.NDArray[np.float64],
) -> float:
    return float(np.linalg.norm(acceleration))


METRICS_EVALUATION: Dict[
    Metric,
    Callable[
        [npt.NDArray[np.float64], npt.NDArray[np.float64], npt.NDArray[np.float64]],
        float,
    ],
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


def performance_evaluation(
    frame: int,
    position: npt.NDArray[np.float64],
    velocity: npt.NDArray[np.float64],
    acceleration: npt.NDArray[np.float64],
    drone_trajectory_performance_check: ErrorMessageList,
) -> None:
    for metric in Metric:
        if not (metric.validation(position, velocity, acceleration)):
            drone_trajectory_performance_check.add_error_message(
                PerformanceInfraction(
                    name=metric.value,
                    frame=frame,
                    value=metric.evaluation(position, velocity, acceleration),
                    threshold=metric.range_.threshold,
                    metric_convention=metric.range_.standard_convention,
                )
            )
