from typing import List

import numpy as np

from ..drones_manager.trajectory_simulation_manager.trajectory_simulation_manager import (
    TrajectorySimulation,
    TrajectorySimulationManager,
)
from ..parameter.parameter import LandParameter, TakeoffParameter, TimecodeParameter
from .dance_simulation.convert_trajectory_to_dance_simulation import (
    convert_trajectory_to_dance_simulation,
)


class ShowSimulationSlice:
    def __init__(self, second: float, nb_drones: int):
        self.second = second
        self.drone_indices = np.array([drone_index for drone_index in range(nb_drones)])
        self.positions = np.zeros((nb_drones, 3))
        self.velocities = np.zeros((nb_drones, 3))
        self.accelerations = np.zeros((nb_drones, 3))
        self.in_air_flags = np.array(nb_drones * [False])
        self.in_dance_flags = np.array(nb_drones * [False])

    @property
    def in_air_drone_indices(self) -> List[int]:
        return list(self.drone_indices[self.in_air_flags])

    @property
    def in_dance_drone_indices(self) -> List[int]:
        return list(self.drone_indices[self.in_dance_flags])


class ShowSimulation:
    def initialize_show_slices(
        self,
        show_second_begin: int,
        last_second: int,
        position_second_rate: int,
    ) -> None:
        bias_second = (
            position_second_rate if not (last_second % position_second_rate) else 0
        )

        self.show_slices = [
            ShowSimulationSlice(
                second,
                self.nb_drones,
            )
            for second in np.arange(
                show_second_begin,
                bias_second + last_second,
                position_second_rate,
            )
        ]

    @property
    def seconds(self) -> List[float]:
        return [show_slice.second for show_slice in self.show_slices]

    def add_dance_simulation(
        self,
        trajectory_simulation: TrajectorySimulation,
        timecode_parameter: TimecodeParameter,
        takeoff_parameter: TakeoffParameter,
        land_parameter: LandParameter,
    ) -> None:
        dance_sequence = convert_trajectory_to_dance_simulation(
            trajectory_simulation,
            self.show_slices[-1].second,
            timecode_parameter,
            takeoff_parameter,
            land_parameter,
        ).dance_sequence
        for show_slice, drone_position, drone_in_air, drone_in_dance in zip(
            self.show_slices,
            dance_sequence.drone_positions,
            dance_sequence.drone_in_air,
            dance_sequence.drone_in_dance,
        ):
            show_slice.positions[trajectory_simulation.drone_index] = drone_position
            show_slice.in_air_flags[trajectory_simulation.drone_index] = drone_in_air
            show_slice.in_dance_flags[
                trajectory_simulation.drone_index
            ] = drone_in_dance

    def update_slices_implicit_values(
        self,
        time_delta: TimecodeParameter,
    ) -> None:
        for slice_index in range(2, len(self.show_slices)):
            self.show_slices[slice_index].velocities = (time_delta) * (
                self.show_slices[slice_index].positions
                - self.show_slices[slice_index - 1].positions
            )
            self.show_slices[slice_index].accelerations = (
                time_delta
                * time_delta
                * (
                    self.show_slices[slice_index].positions
                    - 2 * self.show_slices[slice_index - 1].positions
                    + self.show_slices[slice_index - 2].positions
                )
            )

    def set_slices(
        self,
        trajectory_simulation_manager: TrajectorySimulationManager,
        timecode_parameter: TimecodeParameter,
        takeoff_parameter: TakeoffParameter,
        land_parameter: LandParameter,
    ) -> None:
        self.nb_drones = len(trajectory_simulation_manager.trajectories_simulation)
        self.initialize_show_slices(
            show_second_begin=timecode_parameter.show_second_begin,
            last_second=trajectory_simulation_manager.get_last_second(land_parameter),
            position_second_rate=timecode_parameter.position_second_rate,
        )
        for (
            trajectory_simulation
        ) in trajectory_simulation_manager.trajectories_simulation:
            self.add_dance_simulation(
                trajectory_simulation,
                timecode_parameter,
                takeoff_parameter,
                land_parameter,
            )
        self.update_slices_implicit_values(
            time_delta=1 / (timecode_parameter.position_second_rate)
        )
