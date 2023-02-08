from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


class ShowSimulationSlice:
    def __init__(self, frame: int, nb_drones: int) -> None:
        self.frame = frame
        self._indices = np.array(range(nb_drones), dtype=np.intp)
        self._positions = np.zeros((nb_drones, 3), dtype=np.float64)
        self._in_air_flags = np.array([False for _ in range(nb_drones)], dtype=np.bool_)

    def update_position_air_flag(
        self,
        index: int,
        position: NDArray[np.float64],
        *,
        in_air_flag: bool,
    ) -> None:
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


class ShowSimulation:
    def __init__(self, frames: list[int], nb_drones: int) -> None:
        if nb_drones < 1:
            msg = f"nb_drones must be at least 2, got {nb_drones}"
            raise ValueError(msg)
        self.nb_drones: int = nb_drones
        self.show_slices: list[ShowSimulationSlice] = [
            ShowSimulationSlice(frame, nb_drones) for frame in frames
        ]

    @property
    def frames(self) -> list[int]:
        return [show_slice.frame for show_slice in self.show_slices]
