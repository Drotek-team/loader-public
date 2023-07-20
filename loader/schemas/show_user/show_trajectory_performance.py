from dataclasses import dataclass
from typing import TYPE_CHECKING, List

import numpy as np
from tqdm import tqdm

from loader.parameters import FRAME_PARAMETERS
from loader.schemas.show_user import PositionEventUser, ShowUser

if TYPE_CHECKING:
    from numpy.typing import NDArray


def get_velocities_from_positions(
    frames: List["int"],
    positions: List["NDArray[np.float64]"],
) -> List["NDArray[np.float64]"]:
    if len(positions) == 1:
        return [np.array([0, 0, 0], dtype=np.float64)]
    velocities = [
        1
        / FRAME_PARAMETERS.from_frame_to_second(
            frames[coordinate_index + 1] - frames[coordinate_index],
        )
        * (positions[coordinate_index + 1] - positions[coordinate_index])
        for coordinate_index in range(len(positions) - 1)
    ]
    return [velocities[0], *velocities]


def get_accelerations_from_velocities(
    frames: List["int"],
    velocities: List["NDArray[np.float64]"],
) -> List["NDArray[np.float64]"]:
    if len(velocities) == 1:
        return [np.array([0, 0, 0], dtype=np.float64)]
    accelerations = [
        1
        / FRAME_PARAMETERS.from_frame_to_second(
            frames[coordinate_index + 1] - frames[coordinate_index],
        )
        * (velocities[coordinate_index + 1] - velocities[coordinate_index])
        for coordinate_index in range(len(velocities) - 1)
    ]
    return [accelerations[0], *accelerations]


def get_trajectory_performance_info_from_position_events(
    position_events_user: List["PositionEventUser"],
) -> List["TrajectoryPerformanceInfo"]:
    frames = [position_event.frame for position_event in position_events_user]
    positions = [
        np.array(position_event.xyz, dtype=np.float64) for position_event in position_events_user
    ]
    # Remove the first position if the first position is on the ground
    if len(positions) >= 1 and positions[0][2] == 0:
        frames = frames[1:]
        positions = positions[1:]
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


@dataclass(frozen=True)
class Performance:
    position: "NDArray[np.float64]"
    velocity: "NDArray[np.float64]"
    acceleration: "NDArray[np.float64]"


@dataclass(frozen=True)
class TrajectoryPerformanceInfo:
    frame: int
    performance: Performance

    @property
    def position(self) -> "NDArray[np.float64]":
        return self.performance.position

    @property
    def velocity(self) -> "NDArray[np.float64]":
        return self.performance.velocity

    @property
    def acceleration(self) -> "NDArray[np.float64]":
        return self.performance.acceleration


class DroneTrajectoryPerformance:
    def __init__(
        self,
        index: int,
        trajectory_performance_infos: List["TrajectoryPerformanceInfo"],
    ) -> None:
        self.index = index
        self.trajectory_performance_infos = trajectory_performance_infos

    @classmethod
    def from_show_user(
        cls,
        show_user: ShowUser,
    ) -> List["DroneTrajectoryPerformance"]:
        return [
            cls(
                drone_user.index,
                get_trajectory_performance_info_from_position_events(
                    drone_user.position_events,
                ),
            )
            for drone_user in tqdm(
                show_user.drones_user,
                desc="Computing trajectory performances",
                unit="drone",
            )
        ]
