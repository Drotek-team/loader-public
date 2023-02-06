from typing import Any, List

import numpy as np


class ShowSimulationSlice:
    def __init__(self, frame: int, nb_drones: int):
        self.frame = frame
        self._indices = np.array(range(nb_drones))
        self._positions = np.zeros((nb_drones, 3))
        self._in_air_flags = np.array([False for _ in range(nb_drones)])

    def update_position_air_flag(
        self, index: int, position: Any, *, in_air_flag: bool
    ) -> None:
        self._positions[index] = position
        self._in_air_flags[index] = in_air_flag

    @property
    def in_air_indices(self) -> Any:
        return self._indices[self._in_air_flags]

    @property
    def on_ground_indices(self) -> Any:
        return self._indices[np.invert(self._in_air_flags)]

    @property
    def in_air_positions(self) -> Any:
        return self._positions[self._in_air_flags]

    @property
    def on_ground_positions(self) -> Any:
        return self._positions[np.invert(self._in_air_flags)]


class ShowSimulation:
    def __init__(self, frames: List[int], nb_drones: int):
        if nb_drones < 1:
            msg = f"nb_drones must be at least 2, got {nb_drones}"
            raise ValueError(msg)
        self.nb_drones: int = nb_drones
        self.show_slices: List[ShowSimulationSlice] = [
            ShowSimulationSlice(frame, nb_drones) for frame in frames
        ]

    @property
    def frames(self) -> List[int]:
        return [show_slice.frame for show_slice in self.show_slices]
