from typing import List

import numpy as np


class ShowSimulationSlice:
    def __init__(self, frame: int, nb_drones: int):
        self.frame = frame
        self.drone_indices = np.array([drone_index for drone_index in range(nb_drones)])
        self.positions = np.zeros((nb_drones, 3))
        self.velocities = np.zeros((nb_drones, 3))
        self.accelerations = np.zeros((nb_drones, 3))
        self.in_air_flags = np.array([False for _ in range(nb_drones)])
        self.in_dance_flags = np.array([False for _ in range(nb_drones)])

    @property
    def in_air_drone_indices(self) -> List[int]:
        return list(self.drone_indices[self.in_air_flags])

    @property
    def in_dance_drone_indices(self) -> List[int]:
        return list(self.drone_indices[self.in_dance_flags])


class ShowSimulation:
    def __init__(self, show_slices: List[ShowSimulationSlice]):
        self.nb_drones = len(show_slices[0].drone_indices)
        self.show_slices = show_slices

    @property
    def frames(self) -> List[float]:
        return [show_slice.frame for show_slice in self.show_slices]
