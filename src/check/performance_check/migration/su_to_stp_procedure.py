from typing import List

import numpy as np

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....show_env.show_user.show_user import PositionEventUser, ShowUser
from .show_trajectory_performance import (
    DroneTrajectoryPerformance,
    ShowTrajectoryPerformance,
    TrajectoryPerformanceInfo,
)


def get_trajectory_performance_info_from_position_events(
    position_events_user: List[PositionEventUser],
) -> List[TrajectoryPerformanceInfo]:
    frames = [position_event.frame for position_event in position_events_user]
    positions = [
        np.array(position_event.xyz) for position_event in position_events_user
    ]
    velocities = [
        FRAME_PARAMETER.from_frame_to_second(
            frames[position_index + 1] - frames[position_index]
        )
        * (positions[position_index + 1] - positions[position_index])
        for position_index in range(len(positions) - 1)
    ]
    accelerations = [
        FRAME_PARAMETER.from_frame_to_second(
            frames[velocity_index + 2] - frames[velocity_index + 1]
        )
        * (velocities[velocity_index + 1] - velocities[velocity_index])
        for velocity_index in range(len(velocities) - 1)
    ]
    velocities.insert(0, np.array([0.0, 0.0, 0.0]))
    accelerations.insert(0, np.array([0.0, 0.0, 0.0]))
    accelerations.insert(0, np.array([0.0, 0.0, 0.0]))

    if len(frames) != len(positions) != len(velocities) != len(accelerations):
        msg = "You should have the same number of frames, positions, velocities and accelerations"
        raise ValueError(msg)
    return [
        TrajectoryPerformanceInfo(frame, position, velocity, acceleration)
        for frame, position, velocity, acceleration in zip(
            frames,
            positions,
            velocities,
            accelerations,
        )
    ]


def su_to_stp_procedure(
    show_user: ShowUser,
) -> ShowTrajectoryPerformance:
    return ShowTrajectoryPerformance(
        [
            DroneTrajectoryPerformance(
                drone_index,
                get_trajectory_performance_info_from_position_events(
                    drone_user.position_events[1:],
                ),
            )
            for drone_index, drone_user in enumerate(show_user.drones_user)
        ]
    )
