from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from loader.report.simulation.flight_simulation import get_flight_simulation
from loader.show_env.show_user.show_user import ShowUser

from .show_trajectory_collision import (
    CollisionTrajectory,
    ShowCollisionTrajectory,
)

if TYPE_CHECKING:
    from numpy.typing import NDArray


class ShowPositionFrame:
    def __init__(self, frame: int, drone_indices: list[int]) -> None:
        nb_drones = len(drone_indices)

        self.frame = frame
        self._indices = np.array(drone_indices, dtype=np.intp)
        self._positions = np.zeros((nb_drones, 3), dtype=np.float64)
        self._in_air_flags = np.array([False for _ in range(nb_drones)], dtype=np.bool_)

    def update_position_air_flag(
        self,
        index: int,
        position: NDArray[np.float64],
        *,
        in_air_flag: bool,
    ) -> None:
        index = np.where(self._indices == index)[0][0]
        self._positions[index] = position
        self._in_air_flags[index] = in_air_flag

    @property
    def in_air_indices(self) -> NDArray[np.intp]:
        return self._indices[self._in_air_flags]

    @property
    def on_ground_indices(self) -> NDArray[np.intp]:
        return self._indices[np.invert(self._in_air_flags)]

    @property
    def in_air_positions(self) -> NDArray[np.float64]:
        return self._positions[self._in_air_flags]

    @property
    def on_ground_positions(self) -> NDArray[np.float64]:
        return self._positions[np.invert(self._in_air_flags)]

    def __len__(self) -> int:
        return len(self._indices)


class ShowPositionFrames:
    def __init__(self, frames: list[int], drone_indices: list[int]) -> None:
        nb_drones = len(drone_indices)

        if nb_drones < 1:
            msg = "nb_drones must be at least 1"
            raise ValueError(msg)

        self.show_position_frames: list[ShowPositionFrame] = [
            ShowPositionFrame(frame, drone_indices) for frame in frames
        ]

    @classmethod
    def create_from_show_user(cls, show_user: ShowUser) -> ShowPositionFrames:
        show_collision_trajectory = ShowCollisionTrajectory(
            [
                CollisionTrajectory(
                    drone_user.index,
                    get_flight_simulation(
                        drone_user,
                        show_user.last_frame,
                    ),
                )
                for drone_user in show_user.drones_user
            ],
        )
        show_position_frames = ShowPositionFrames(
            frames=show_collision_trajectory.frames,
            drone_indices=list(range(show_collision_trajectory.drone_number)),
        )
        for collision_trajectory in show_collision_trajectory:
            for show_slice, collision_position_infos in zip(
                show_position_frames.show_position_frames,
                collision_trajectory.collision_position_infos,
            ):
                show_slice.update_position_air_flag(
                    collision_trajectory.drone_index,
                    collision_position_infos.position,
                    in_air_flag=collision_position_infos.in_air,
                )
        return show_position_frames

    @classmethod
    def create_from_frames_positions(
        cls,
        frame_start: int,
        frame_end: int,
        drone_indices: list[int],
        frames_positions: list[list[tuple[float, float, float]]],
    ) -> ShowPositionFrames:
        if frame_start >= frame_end:
            msg = f"frame_start must be strictly smaller than frame_end, not {frame_start} and {frame_end}"
            raise ValueError(msg)

        if frame_end - frame_start != len(frames_positions):
            msg = (
                f"frame_end - frame_start must be equal to the length of frames_positions, "
                f"not {frame_end - frame_start} and {len(frames_positions)}"
            )
            raise ValueError(msg)

        if any(len(drone_indices) != len(positions) for positions in frames_positions):
            msg = "drone_indices and frames_positions items must have the same length"
            raise ValueError(msg)

        show_position_frames = ShowPositionFrames(
            frames=list(
                range(
                    frame_start,
                    frame_end,
                ),
            ),
            drone_indices=drone_indices,
        )
        for show_slice, positions in zip(
            show_position_frames.show_position_frames,
            frames_positions,
        ):
            for index, position in zip(drone_indices, positions):
                show_slice.update_position_air_flag(
                    index,
                    np.array(position),
                    in_air_flag=position[2] != 0,
                )
        return show_position_frames
