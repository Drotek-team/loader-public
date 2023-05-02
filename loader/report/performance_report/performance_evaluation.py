import itertools
from enum import Enum
from typing import List, Optional, Tuple

import numpy as np

from loader.parameter.iostar_physic_parameter import (
    IOSTAR_PHYSIC_PARAMETER_MAX,
    IOSTAR_PHYSIC_PARAMETER_RECOMMENDATION,
    IostarPhysicParameter,
)
from loader.report.base import BaseInfraction
from loader.report.performance_report.migration.show_trajectory_performance import (
    Performance,
)

from .migration.show_trajectory_performance import (
    DroneTrajectoryPerformance,
    ShowTrajectoryPerformance,
)


class PerformanceKind(Enum):
    HORIZONTAL_VELOCITY = "horizontal velocity"
    UP_VELOCITY = "up velocity"
    DOWN_VELOCITY = "down velocity"
    ACCELERATION = "acceleration"

    def check(
        self,
        physic_parameter: IostarPhysicParameter,
        performance: Performance,
    ) -> Tuple[bool, float, float]:
        """Check if the performance is above the threshold."""
        if self == PerformanceKind.HORIZONTAL_VELOCITY:
            threshold = physic_parameter.horizontal_velocity_max
            value = float(np.linalg.norm(performance.velocity[0:2]))
        elif self == PerformanceKind.UP_VELOCITY:
            threshold = physic_parameter.velocity_up_max
            value = float(performance.velocity[2])
        elif self == PerformanceKind.DOWN_VELOCITY:
            threshold = physic_parameter.velocity_down_max
            value = float(-performance.velocity[2])
        elif self == PerformanceKind.ACCELERATION:
            threshold = physic_parameter.acceleration_max
            value = float(np.linalg.norm(performance.acceleration))
        else:  # pragma: no cover
            msg = f"PerformanceKind {self} not implemented in check_performance()."
            raise NotImplementedError(msg)

        return value > threshold, threshold, value


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
        physic_parameter: IostarPhysicParameter,
    ) -> List["PerformanceInfraction"]:
        performance_infractions: List["PerformanceInfraction"] = []
        for performance_kind in PerformanceKind:
            is_infraction, threshold, value = performance_kind.check(
                physic_parameter,
                performance,
            )
            if is_infraction:
                performance_infractions.append(
                    PerformanceInfraction(
                        performance_name=performance_kind.value,
                        drone_index=drone_index,
                        frame=frame,
                        value=value,
                        threshold=threshold,
                    ),
                )
        return performance_infractions

    @classmethod
    def _get_performance_infractions_from_drone_performance(
        cls,
        drone_trajectory_performance: DroneTrajectoryPerformance,
        physic_parameter: IostarPhysicParameter,
    ) -> List["PerformanceInfraction"]:
        return list(
            itertools.chain.from_iterable(
                cls._get_performance_infractions_from_performance(
                    drone_trajectory_performance.index,
                    trajectory_performance_info.frame,
                    trajectory_performance_info.performance,
                    physic_parameter,
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
        *,
        physic_parameter: Optional[IostarPhysicParameter] = None,
    ) -> List["PerformanceInfraction"]:
        if physic_parameter is None:
            physic_parameter = IOSTAR_PHYSIC_PARAMETER_RECOMMENDATION
        else:
            if (
                physic_parameter.horizontal_velocity_max
                > IOSTAR_PHYSIC_PARAMETER_MAX.horizontal_velocity_max
            ):
                msg = f"Horizontal velocity max {physic_parameter.horizontal_velocity_max} is greater than {IOSTAR_PHYSIC_PARAMETER_MAX.horizontal_velocity_max}"
                raise ValueError(msg)
            if physic_parameter.velocity_up_max > IOSTAR_PHYSIC_PARAMETER_MAX.velocity_up_max:
                msg = f"Up velocity max {physic_parameter.velocity_up_max} is greater than {IOSTAR_PHYSIC_PARAMETER_MAX.velocity_up_max}"
                raise ValueError(msg)
            if physic_parameter.velocity_down_max > IOSTAR_PHYSIC_PARAMETER_MAX.velocity_down_max:
                msg = f"Down velocity max {physic_parameter.velocity_down_max} is greater than {IOSTAR_PHYSIC_PARAMETER_MAX.velocity_down_max}"
                raise ValueError(msg)
            if physic_parameter.acceleration_max > IOSTAR_PHYSIC_PARAMETER_MAX.acceleration_max:
                msg = f"Acceleration max {physic_parameter.acceleration_max} is greater than {IOSTAR_PHYSIC_PARAMETER_MAX.acceleration_max}"
                raise ValueError(msg)

        return list(
            itertools.chain.from_iterable(
                cls._get_performance_infractions_from_drone_performance(
                    drone_trajectory_performance,
                    physic_parameter,
                )
                for (
                    drone_trajectory_performance
                ) in show_trajectory_performance.drones_trajectory_performance
            ),
        )
