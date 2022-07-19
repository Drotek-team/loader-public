from dataclasses import dataclass
from typing import List

import numpy as np

from ...parameter.parameter import JsonConvertionConstant, LandParameter
from ..drone.events.position_events import PositionEvent


@dataclass(frozen=True)
class PositionSimulation:
    second: float
    xyz: np.ndarray


@dataclass
class TrajectorySimulation:
    drone_index: int

    def initialize_position_simulation(
        self,
        position_events: List[PositionEvent],
        json_convertion_constant: JsonConvertionConstant,
    ) -> None:

        self.positions_simulation = [
            PositionSimulation(
                json_convertion_constant.TIMECODE_TO_SECOND_RATIO
                * position_event.timecode,
                json_convertion_constant.from_json_position_to_simulation_position(
                    position_event.get_values()
                ),
            )
            for position_event in position_events
        ]

    @property
    def last_second(self) -> float:
        return self.positions_simulation[-1].second

    @property
    def last_height(self) -> float:
        return self.positions_simulation[-1].xyz[2]


class TrajectorySimulationManager:
    def __init__(self, nb_drones: int):
        self.trajectories_simulation = [
            TrajectorySimulation(drone_index) for drone_index in range(nb_drones)
        ]

    def get_last_second(self, land_parameter: LandParameter) -> float:
        return max(
            trajectory_simulation.last_second
            + land_parameter.get_land_second_delta(trajectory_simulation.last_height)
            for trajectory_simulation in self.trajectories_simulation
        )
