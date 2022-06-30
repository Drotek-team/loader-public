from typing import List

import numpy as np

from ..drones_manager.drone.events.position_events import PositionEvent
from ..parameter.parameter import (
    JsonConventionConstant,
    LandParameter,
    TimecodeParameter,
)


class ShowSimulationSlice:
    def __init__(self, timecode: int, nb_drones: int):
        self.timecode = timecode
        self.drone_indices = np.array([drone_index for drone_index in range(nb_drones)])
        self.positions = np.zeros((nb_drones, 3))
        self.velocities = np.zeros((nb_drones, 3))
        self.accelerations = np.zeros((nb_drones, 3))
        self.in_air_flags = np.array(nb_drones * [False])
        self.in_dance_flags = np.array(nb_drones * [False])


class ShowSimulation:
    def __init__(
        self,
        nb_drones: int,
        timecode_parameter: TimecodeParameter,
    ):
        self.nb_drones = nb_drones
        self.position_timecode_rate = timecode_parameter.position_timecode_rate
        self.show_slices: List[ShowSimulationSlice] = []

    def update_show_slices(
        self,
        last_position_events: List[PositionEvent],
        land_parameter: LandParameter,
        json_convention_constant: JsonConventionConstant,
    ):

        last_simulation_timecode = max(
            last_position_event.timecode
            + land_parameter.get_second_land_timecode_delta(
                json_convention_constant.CENTIMETER_TO_METER_RATIO
                * last_position_event.z
            )
            for last_position_event in last_position_events
        )
        self.show_slices = [
            ShowSimulationSlice(
                self.position_timecode_rate * timecode_index,
                self.nb_drones,
            )
            for timecode_index in range(
                (last_simulation_timecode // self.position_timecode_rate) + 1
            )
        ]

    @property
    def timecodes(self) -> List[int]:
        return [show_slice.timecode for show_slice in self.show_slices]

    def add_dance_simulation(
        self,
        drone_index: int,
        drone_positions: List[np.ndarray],
        drone_in_air_flags: List[bool],
        drone_in_dance_flags: List[bool],
    ) -> None:
        for (slice, drone_position, drone_in_air_index, drone_in_dance_index,) in zip(
            self.show_slices,
            drone_positions,
            drone_in_air_flags,
            drone_in_dance_flags,
        ):
            slice.positions[drone_index] = drone_position
            slice.in_air_flags[drone_index] = drone_in_air_index
            slice.in_dance_flags[drone_index] = drone_in_dance_index

    def update_slices_implicit_values(
        self,
    ) -> None:
        for slice_index in range(2, len(self.show_slices)):
            self.show_slices[slice_index].velocities = (1 / self.position_time_rate) * (
                self.show_slices[slice_index].positions
                - self.show_slices[slice_index - 1].positions
            )
            self.show_slices[slice_index].accelerations = (
                1
                / (self.position_time_rate * self.position_time_rate)
                * (
                    self.show_slices[slice_index].positions
                    - 2 * self.show_slices[slice_index - 1].positions
                    + self.show_slices[slice_index - 1].positions
                )
            )
