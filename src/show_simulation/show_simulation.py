from typing import List

import numpy as np

from ..drones_manager.drone.events.position_events import PositionEvent
from ..drones_manager.drones_manager import Drone
from ..parameter.parameter import (
    JsonConventionConstant,
    LandParameter,
    TakeoffParameter,
    TimecodeParameter,
)
from .dance_simulation.convert_drone_to_dance_simulation import (
    convert_drone_to_dance_simulation,
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
        drone: Drone,
        timecode_parameter: TimecodeParameter,
        takeoff_parameter: TakeoffParameter,
        land_parameter: LandParameter,
        json_convention_constant: JsonConventionConstant,
    ) -> None:
        dance_sequence = convert_drone_to_dance_simulation(
            drone,
            self.show_slices[-1].timecode,
            timecode_parameter,
            takeoff_parameter,
            land_parameter,
            json_convention_constant,
        ).dance_sequence
        for show_slice, drone_position, drone_in_air, drone_in_dance in zip(
            self.show_slices,
            dance_sequence.drone_positions,
            dance_sequence.drone_in_air,
            dance_sequence.drone_in_dance,
        ):
            show_slice.positions[drone.index] = drone_position
            show_slice.in_air_flags[drone.index] = drone_in_air
            show_slice.in_dance_flags[drone.index] = drone_in_dance

    def update_slices_implicit_values(
        self,
    ) -> None:
        for slice_index in range(2, len(self.show_slices)):
            self.show_slices[slice_index].velocities = (
                1 / self.position_timecode_rate
            ) * (
                self.show_slices[slice_index].positions
                - self.show_slices[slice_index - 1].positions
            )
            self.show_slices[slice_index].accelerations = (
                1
                / (self.position_timecode_rate * self.position_timecode_rate)
                * (
                    self.show_slices[slice_index].positions
                    - 2 * self.show_slices[slice_index - 1].positions
                    + self.show_slices[slice_index - 1].positions
                )
            )
