from typing import List

import numpy as np
from script.json_manager.parameter.parameter import TimecodeParameter


class ShowSimulationSlice:
    def __init__(self, nb_drones: int, position_size: int):
        self.drone_indices = np.array([drone_index for drone_index in range(nb_drones)])
        self.positions = np.zeros((nb_drones, position_size))
        self.velocities = np.zeros((nb_drones, position_size))
        self.accelerations = np.zeros((nb_drones, position_size))
        self.in_air_indices = np.array(nb_drones * [False])
        self.in_dance_indices = np.array(nb_drones * [False])


class ShowSimulation:
    def __init__(
        self,
        nb_drones: int,
        nb_slices: int,
        position_time_rate: int,
        position_size: int,
    ):
        self.nb_drones = nb_drones
        self.position_time_rate = position_time_rate
        self.slices = {
            position_time_rate
            * time_index: ShowSimulationSlice(nb_drones, position_size)
            for time_index in range(nb_slices)
        }

    def add_dance_simulation(
        self,
        drone_index: int,
        drone_positions: List[np.ndarray],
        drone_in_air_indices: List[bool],
        drone_in_dance_indices: List[bool],
    ) -> None:
        for (time, drone_position, drone_in_air_index, drone_in_dance_index,) in zip(
            self.slices.keys(),
            drone_positions,
            drone_in_air_indices,
            drone_in_dance_indices,
        ):
            self.slices[time].positions[drone_index] = drone_position
            self.slices[time].in_air_indices[drone_index] = drone_in_air_index
            self.slices[time].in_dance_indices[drone_index] = drone_in_dance_index

    def update_slices_implicit_values(
        self,
    ) -> None:
        for slice_index in range(2, len(self.slices)):
            self.slices[slice_index].velocities = self.position_time_rate * (
                self.slices[slice_index].positions
                - self.slices[slice_index - 1].positions
            )
            self.slices[slice_index].velocities = (
                self.position_time_rate
                * self.position_time_rate
                * (
                    self.slices[slice_index].positions
                    - 2 * self.slices[slice_index - 1].positions
                    + self.slices[slice_index - 1].positions
                )
            )
