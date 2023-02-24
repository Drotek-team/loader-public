from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from loader.parameter.iostar_dance_import_parameter.frame_parameter import (
    FRAME_PARAMETER,
)
from loader.show_env.show_user import PositionEventUser, ShowUser

from .show_trajectory_performance import (
    DroneTrajectoryPerformance,
    Performance,
    ShowTrajectoryPerformance,
    TrajectoryPerformanceInfo,
)

if TYPE_CHECKING:
    from numpy.typing import NDArray


def get_velocities_from_positions(
    frames: list[int],
    positions: list[NDArray[np.float64]],
) -> list[NDArray[np.float64]]:
    if len(positions) == 1:
        return [np.array([0, 0, 0], dtype=np.float64)]
    extended_frames = [frames[0] - 1, *frames]
    extended_positions = [positions[0], *positions]
    return [
        1
        / FRAME_PARAMETER.from_frame_to_second(
            extended_frames[coordinate_index] - extended_frames[coordinate_index - 1],
        )
        * (
            extended_positions[coordinate_index]
            - extended_positions[coordinate_index - 1]
        )
        for coordinate_index in range(1, len(positions) + 1)
    ]


def get_accelerations_from_velocities(
    frames: list[int],
    velocities: list[NDArray[np.float64]],
) -> list[NDArray[np.float64]]:
    if len(velocities) == 1:
        return [np.array([0, 0, 0], dtype=np.float64)]
    extended_frames = [frames[0] - 1, *frames]
    extended_velocities = [velocities[0], *velocities]
    return [
        1
        / FRAME_PARAMETER.from_frame_to_second(
            extended_frames[coordinate_index] - extended_frames[coordinate_index - 1],
        )
        * (
            extended_velocities[coordinate_index]
            - extended_velocities[coordinate_index - 1]
        )
        for coordinate_index in range(1, len(velocities) + 1)
    ]


def get_trajectory_performance_info_from_position_events(
    position_events_user: list[PositionEventUser],
) -> list[TrajectoryPerformanceInfo]:
    frames = [position_event.frame for position_event in position_events_user]
    positions = [
        np.array(position_event.xyz, dtype=np.float64)
        for position_event in position_events_user
    ]
    velocities = get_velocities_from_positions(frames, positions)
    accelerations = get_accelerations_from_velocities(frames, velocities)

    return [
        TrajectoryPerformanceInfo(frame, Performance(position, velocity, acceleration))
        for frame, position, velocity, acceleration in zip(
            frames,
            positions,
            velocities,
            accelerations,
        )
    ]


def su_to_stp(
    show_user: ShowUser,
) -> ShowTrajectoryPerformance:
    return ShowTrajectoryPerformance(
        [
            DroneTrajectoryPerformance(
                drone_user.index,
                get_trajectory_performance_info_from_position_events(
                    drone_user.position_events,
                ),
            )
            for drone_user in show_user.drones_user
        ],
    )
