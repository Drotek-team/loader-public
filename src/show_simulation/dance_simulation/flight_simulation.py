from typing import List

import numpy as np

from ...drones_manager.trajectory_simulation_manager.trajectory_simulation_manager import (
    PositionSimulation,
)
from ...parameter.parameter import TimecodeParameter
from .dance_simulation import DanceSequence
from .position_simulation import linear_interpolation


def flight_simulation(
    position_simulation_list: List[PositionSimulation],
    timecode_parameter: TimecodeParameter,
) -> DanceSequence:
    flight_positions: List[np.ndarray] = []
    for position_simulation, next_position_simulation_list in zip(
        position_simulation_list[:-1], position_simulation_list[1:]
    ):
        flight_positions += linear_interpolation(
            position_simulation.xyz,
            next_position_simulation_list.xyz,
            int(
                ((next_position_simulation_list.second - position_simulation.second))
                / timecode_parameter.position_second_rate
            ),
        )
    return DanceSequence(
        flight_positions, len(flight_positions) * [True], len(flight_positions) * [True]
    )
