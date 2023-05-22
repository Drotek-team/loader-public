# pyright: reportIncompatibleMethodOverride=false
import itertools
from enum import Enum
from typing import List, Optional, Tuple

import numpy as np

from loader.parameters import (
    IOSTAR_PHYSIC_PARAMETERS_MAX,
    IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION,
    IostarPhysicParameters,
)
from loader.reports.base import BaseInfraction
from loader.schemas import ShowUser
from loader.schemas.show_user.show_trajectory_performance import (
    DroneTrajectoryPerformance,
    Performance,
)


class PerformanceKind(Enum):
    HORIZONTAL_VELOCITY = "horizontal velocity"
    UP_VELOCITY = "up velocity"
    DOWN_VELOCITY = "down velocity"
    ACCELERATION = "acceleration"

    def check(
        self,
        physic_parameters: IostarPhysicParameters,
        performance: Performance,
    ) -> Tuple[bool, float, float]:
        """Check if the performance is above the threshold."""
        if self == PerformanceKind.HORIZONTAL_VELOCITY:
            threshold = physic_parameters.horizontal_velocity_max
            value = float(np.linalg.norm(performance.velocity[0:2]))
        elif self == PerformanceKind.UP_VELOCITY:
            threshold = physic_parameters.velocity_up_max
            value = float(performance.velocity[2])
        elif self == PerformanceKind.DOWN_VELOCITY:
            threshold = physic_parameters.velocity_down_max
            value = float(-performance.velocity[2])
        elif self == PerformanceKind.ACCELERATION:
            threshold = physic_parameters.acceleration_max
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
        physic_parameters: IostarPhysicParameters,
    ) -> List["PerformanceInfraction"]:
        performance_infractions: List["PerformanceInfraction"] = []
        for performance_kind in PerformanceKind:
            is_infraction, threshold, value = performance_kind.check(
                physic_parameters,
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
        physic_parameters: IostarPhysicParameters,
    ) -> List["PerformanceInfraction"]:
        return list(
            itertools.chain.from_iterable(
                cls._get_performance_infractions_from_performance(
                    drone_trajectory_performance.index,
                    trajectory_performance_info.frame,
                    trajectory_performance_info.performance,
                    physic_parameters,
                )
                for (
                    trajectory_performance_info
                ) in drone_trajectory_performance.trajectory_performance_infos
            ),
        )

    @classmethod
    def generate(
        cls,
        show_user: ShowUser,
        *,
        physic_parameters: Optional[IostarPhysicParameters] = None,
    ) -> List["PerformanceInfraction"]:
        show_trajectory_performance = DroneTrajectoryPerformance.from_show_user(show_user)
        if physic_parameters is None:
            physic_parameters = IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION
        else:
            if (
                physic_parameters.horizontal_velocity_max
                > IOSTAR_PHYSIC_PARAMETERS_MAX.horizontal_velocity_max
            ):
                msg = f"Horizontal velocity max {physic_parameters.horizontal_velocity_max} is greater than {IOSTAR_PHYSIC_PARAMETERS_MAX.horizontal_velocity_max}"
                raise ValueError(msg)
            if physic_parameters.velocity_up_max > IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_up_max:
                msg = f"Up velocity max {physic_parameters.velocity_up_max} is greater than {IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_up_max}"
                raise ValueError(msg)
            if physic_parameters.velocity_down_max > IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_down_max:
                msg = f"Down velocity max {physic_parameters.velocity_down_max} is greater than {IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_down_max}"
                raise ValueError(msg)
            if physic_parameters.acceleration_max > IOSTAR_PHYSIC_PARAMETERS_MAX.acceleration_max:
                msg = f"Acceleration max {physic_parameters.acceleration_max} is greater than {IOSTAR_PHYSIC_PARAMETERS_MAX.acceleration_max}"
                raise ValueError(msg)

        return list(
            itertools.chain.from_iterable(
                cls._get_performance_infractions_from_drone_performance(
                    drone_trajectory_performance,
                    physic_parameters,
                )
                for drone_trajectory_performance in show_trajectory_performance
            ),
        )
