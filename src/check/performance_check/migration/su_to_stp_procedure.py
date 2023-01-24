from typing import List

import numpy as np
import numpy.typing as npt

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....show_env.show_user.show_user import PositionEventUser, ShowUser
from .show_trajectory_performance import (
    DroneTrajectoryPerformance,
    Performance,
    ShowTrajectoryPerformance,
    TrajectoryPerformanceInfo,
)


def get_velocities_from_positions(
    frames: List[int], positions: List[npt.NDArray[np.float64]]
) -> List[npt.NDArray[np.float64]]:
    extended_frames = [frames[0] - 1] + frames
    extended_positions = [positions[0]] + positions
    return [
        FRAME_PARAMETER.from_frame_to_second(
            extended_frames[coordinate_index] - extended_frames[coordinate_index - 1]
        )
        * (
            extended_positions[coordinate_index]
            - extended_positions[coordinate_index - 1]
        )
        for coordinate_index in range(1, len(positions) + 1)
    ]


def get_accelerations_from_velocities(
    frames: List[int], velocities: List[npt.NDArray[np.float64]]
) -> List[npt.NDArray[np.float64]]:
    extended_frames = [frames[0] - 1] + frames
    extended_velocities = [velocities[0]] + velocities
    return [
        FRAME_PARAMETER.from_frame_to_second(
            extended_frames[coordinate_index] - extended_frames[coordinate_index - 1]
        )
        * (
            extended_velocities[coordinate_index]
            - extended_velocities[coordinate_index - 1]
        )
        for coordinate_index in range(1, len(velocities) + 1)
    ]


def get_trajectory_performance_info_from_position_events(
    position_events_user: List[PositionEventUser],
) -> List[TrajectoryPerformanceInfo]:
    frames = [position_event.frame for position_event in position_events_user]
    positions = [
        np.array(position_event.xyz) for position_event in position_events_user
    ]
    velocities = get_velocities_from_positions(frames, positions)
    accelerations = get_accelerations_from_velocities(frames, velocities)

    if len(frames) != len(positions) != len(velocities) != len(accelerations):
        msg = "You should have the same number of frames, positions, velocities and accelerations"
        raise ValueError(msg)
    return [
        TrajectoryPerformanceInfo(frame, Performance(position, velocity, acceleration))
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
                    drone_user.flight_positions,
                ),
            )
            for drone_index, drone_user in enumerate(show_user.drones_user)
        ]
    )
