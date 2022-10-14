from typing import List
from ...parameter.parameter import FrameParameter

from ...show_trajectory_performance.show_trajectory_performance import (
    ShowTrajectoryPerformance,
)
from ...show_dev.show_dev import ShowDev
from .simulation.in_air_flight_simulation import in_air_flight_simulation
from .simulation.position_simulation import SimulationInfo
from ...show_trajectory_performance.show_trajectory_performance import (
    TrajectoryPerformanceInfo,
    DroneTrajectoryPerformance,
)
import numpy as np

VELOCITY_ESTIMATION_INDEX = 1
ACCELERATION_ESTIMATION_INDEX = 2


def get_trajectory_performance_info_from_simulation_infos(
    simulation_infos: List[SimulationInfo], frame_parameter: FrameParameter
) -> List[TrajectoryPerformanceInfo]:
    positions = [simulation_info.position for simulation_info in simulation_infos]
    velocities = [np.array((0.0, 0.0, 0.0)),] + [
        frame_parameter.position_fps
        * (
            positions[simulation_index]
            - positions[simulation_index - VELOCITY_ESTIMATION_INDEX]
        )
        for simulation_index in range(VELOCITY_ESTIMATION_INDEX, len(simulation_infos))
    ]
    accelerations: List[np.ndarray] = [
        np.array((0.0, 0.0, 0.0)),
        np.array((0.0, 0.0, 0.0)),
    ] + [
        frame_parameter.position_fps
        * frame_parameter.position_fps
        * (
            positions[simulation_index]
            - 2 * positions[simulation_index - VELOCITY_ESTIMATION_INDEX]
            + positions[simulation_index - ACCELERATION_ESTIMATION_INDEX]
        )
        for simulation_index in range(
            ACCELERATION_ESTIMATION_INDEX, len(simulation_infos)
        )
    ]

    return [
        TrajectoryPerformanceInfo(
            simulation_info.frame, simulation_info.position, velocity, acceleration
        )
        for simulation_info, velocity, acceleration in zip(
            simulation_infos, velocities, accelerations
        )
    ]


def SD_to_STP_procedure(
    show_dev: ShowDev,
    frame_parameter: FrameParameter,
) -> ShowTrajectoryPerformance:
    return ShowTrajectoryPerformance(
        [
            DroneTrajectoryPerformance(
                drone_dev.drone_index,
                get_trajectory_performance_info_from_simulation_infos(
                    in_air_flight_simulation(
                        drone_dev.position_events_dev[1:],
                    ),
                    frame_parameter,
                ),
            )
            for drone_dev in show_dev.drones_dev
        ]
    )
