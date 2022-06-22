from typing import List

import numpy as np

from ......parameter.parameter import IostarParameter, TakeoffParameter
from .ratio_manager import Metric, OneSizedRatio, TwoSizedRatio


class ObservedMetrics:
    def __init__(
        self,
        iostar_parameter: IostarParameter,
        takeoff_parameter: TakeoffParameter,
    ):
        self.position_z = Metric(
            "position Z performance",
            OneSizedRatio(0, takeoff_parameter.takeoff_altitude, False),
        )
        self.velocity_h = Metric(
            "horizontal velocity performance",
            OneSizedRatio(0, iostar_parameter.horizontal_velocity_max),
        )
        self.acceleration_h = Metric(
            "horizontal acceleration performance",
            OneSizedRatio(0, iostar_parameter.horizontal_acceleration_max),
        )
        self.force_up = Metric(
            "force up performance", OneSizedRatio(0, iostar_parameter.force_up_max)
        )
        self.force_down = Metric(
            "force down performance",
            OneSizedRatio(-iostar_parameter.force_down_max, 0, False),
        )

    @staticmethod
    def force_evaluation(
        velocity: np.ndarray, acceleration: np.ndarray, mass: float, drag_coef: float
    ) -> float:
        if len(velocity) > 1:
            return float(
                mass * np.linalg.norm(acceleration)
                + drag_coef * np.square(np.linalg.norm(velocity))
            )
        else:
            return float(
                mass * acceleration
                + np.sign(velocity) * drag_coef * np.square(velocity)
            )

    def update_metrics(
        self,
        position: np.ndarray,
        velocity: np.ndarray,
        acceleration: np.ndarray,
        iostar_parameter: IostarParameter,
    ) -> None:
        self.position_z.update(position[2])
        self.velocity_h.update(np.linalg.norm(velocity[0:2]))
        self.acceleration_h.update(np.linalg.norm(acceleration[0:2]))
        self.force_up.update(
            self.force_evaluation(
                velocity,
                acceleration,
                iostar_parameter.iostar_mass,
                iostar_parameter.iostar_drag_vertical_coef,
            )
        )
        self.force_down.update(
            self.force_evaluation(
                velocity,
                acceleration,
                iostar_parameter.iostar_mass,
                iostar_parameter.iostar_drag_vertical_coef,
            )
        )

    def get_metrics(self) -> List[Metric]:
        return [
            self.position_z,
            self.velocity_h,
            self.acceleration_h,
            self.force_up,
            self.force_down,
        ]
