from typing import List

import numpy as np

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...show_dev.show_dev import ShowDev
from ...show_trajectory_performance.show_trajectory_performance import (
    DroneTrajectoryPerformance,
    ShowTrajectoryPerformance,
    TrajectoryPerformanceInfo,
)
from .simulation.in_air_flight_simulation import in_air_flight_simulation
from .simulation.position_simulation import SimulationInfo

VELOCITY_ESTIMATION_INDEX = 1
ACCELERATION_ESTIMATION_INDEX = 2


def get_trajectory_performance_info_from_simulation_infos(
    simulation_infos: List[SimulationInfo],
) -> List[TrajectoryPerformanceInfo]:
    positions = [simulation_infos[0].position, simulation_infos[0].position] + [
        simulation_info.position for simulation_info in simulation_infos
    ]
    velocities = [
        FRAME_PARAMETER.position_fps
        * (
            positions[position_index]
            - positions[position_index - VELOCITY_ESTIMATION_INDEX]
        )
        for position_index in range(len(positions))
    ]
    accelerations: List[np.ndarray] = [
        FRAME_PARAMETER.position_fps
        * FRAME_PARAMETER.position_fps
        * (
            positions[position_index]
            - 2 * positions[position_index - VELOCITY_ESTIMATION_INDEX]
            + positions[position_index - ACCELERATION_ESTIMATION_INDEX]
        )
        for position_index in range(len(positions))
    ]

    return [
        TrajectoryPerformanceInfo(
            simulation_info.frame, position, velocity, acceleration
        )
        for simulation_info, position, velocity, acceleration in zip(
            simulation_infos,
            positions[ACCELERATION_ESTIMATION_INDEX:],
            velocities[ACCELERATION_ESTIMATION_INDEX:],
            accelerations[ACCELERATION_ESTIMATION_INDEX:],
        )
    ]


def SD_to_STP_procedure(
    show_dev: ShowDev,
) -> ShowTrajectoryPerformance:
    return ShowTrajectoryPerformance(
        [
            DroneTrajectoryPerformance(
                drone_dev.drone_index,
                get_trajectory_performance_info_from_simulation_infos(
                    in_air_flight_simulation(
                        drone_dev.position_events_dev[1:],
                    ),
                ),
            )
            for drone_dev in show_dev.drones_dev
        ]
    )
