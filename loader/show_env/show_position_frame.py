from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from loader.report.simulation.flight_simulation import (
    get_flight_simulation,
    get_partial_flight_simulation,
)
from loader.show_env.show_user.show_user import ShowUser

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

    @classmethod
    def from_show_user(
        cls,
        show_user: ShowUser,
        *,
        is_partial: bool,
    ) -> list[ShowPositionFrame]:
        drone_indices = [drone_user.index for drone_user in show_user.drones_user]
        flight_simulations = [
            get_partial_flight_simulation(drone_user)
            if is_partial
            else get_flight_simulation(drone_user, show_user.last_frame)
            for drone_user in show_user.drones_user
        ]
        show_position_frames = [
            ShowPositionFrame(frame, drone_indices)
            for frame in range(
                min(flight_simulation[0].frame for flight_simulation in flight_simulations),
                max(flight_simulation[-1].frame for flight_simulation in flight_simulations) + 1,
            )
        ]
        for drone_index, flight_simulation in zip(drone_indices, flight_simulations):
            for show_slice, simulation_info in zip(show_position_frames, flight_simulation):
                show_slice.update_position_air_flag(
                    drone_index,
                    simulation_info.position,
                    in_air_flag=simulation_info.in_air,
                )
        return show_position_frames
