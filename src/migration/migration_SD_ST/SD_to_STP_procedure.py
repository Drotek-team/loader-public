from typing import List
from ...parameter.parameter import LandParameter, TakeoffParameter, FrameParameter

from ...show_trajectory_performance.show_trajectory_performance import (
    ShowTrajectoryPerformance,
)
from ...show_dev.show_dev import ShowDev
from .simulation.in_air_flight_simulation import in_air_flight_simulation
from .simulation.position_simulation import SimulationInfo
from ...show_trajectory_performance.show_trajectory_performance import (
    TrajectoryPerformanceInfo,
)
import numpy as np

VELOCITY_ESTIMATION_INDEX = 1
ACCELERATION_ESTIMATION_INDEX = 2


def get_trajectory_performance_info_from_simulation_infos(
    simulation_infos: List[SimulationInfo], position_fps: int
) -> List[TrajectoryPerformanceInfo]:
    positions_array = np.array(
        [simulation_info.position for simulation_info in simulation_infos]
    )

    velocities_array = np.concatenate(
        (np.array([0]), position_fps * (positions_array[1:] - positions_array[:-1]))
    )
    accelerations_array = np.concatenate(
        (np.array([0]), position_fps * (velocities_array[1:] - velocities_array[:-1]))
    )
    return [
        TrajectoryPerformanceInfo(position, velocity, acceleration)
        for position, velocity, acceleration in zip(
            positions_array, velocities_array, accelerations_array
        )
    ]


def SD_to_ST_procedure(
    show_dev: ShowDev,
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
    land_parameter: LandParameter,
) -> ShowTrajectoryPerformance:
    return ShowTrajectoryPerformance(
        [
            in_air_flight_simulation(
                drone_dev,
                frame_parameter,
                takeoff_parameter,
                land_parameter,
            )
            for drone_dev in show_dev.drones_dev
        ]
    )
