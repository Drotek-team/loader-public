from typing import List

import numpy as np
import numpy.typing as npt

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....show_env.show_user.show_user import ShowUser
from ...simulation.in_air_flight_simulation import in_air_flight_simulation
from ...simulation.position_simulation import SimulationInfo
from .show_trajectory_performance import (
    DroneTrajectoryPerformance,
    ShowTrajectoryPerformance,
    TrajectoryPerformanceInfo,
)

VELOCITY_ESTIMATION_INDEX = 1
ACCELERATION_ESTIMATION_INDEX = 2


def get_trajectory_performance_info_from_simulation_infos(
    simulation_infos: List[SimulationInfo],
) -> List[TrajectoryPerformanceInfo]:
    positions = [simulation_infos[0].position, simulation_infos[0].position] + [
        simulation_info.position for simulation_info in simulation_infos
    ]
    # TODO: WARNING if the sampling frequence is different from _fps, this calculus is wrong
    velocities = [
        FRAME_PARAMETER.from_second_to_frame(1)
        * (
            positions[position_index]
            - positions[position_index - VELOCITY_ESTIMATION_INDEX]
        )
        for position_index in range(len(positions))
    ]
    accelerations: List[npt.NDArray[np.float64]] = [
        FRAME_PARAMETER.from_second_to_frame(1)
        * FRAME_PARAMETER.from_second_to_frame(1)
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


def su_to_stp_procedure(
    show_user: ShowUser,
) -> ShowTrajectoryPerformance:
    return ShowTrajectoryPerformance(
        [
            DroneTrajectoryPerformance(
                drone_index,
                get_trajectory_performance_info_from_simulation_infos(
                    in_air_flight_simulation(
                        drone_user.position_events[1:],
                    ),
                ),
            )
            for drone_index, drone_user in enumerate(show_user.drones_user)
        ]
    )
