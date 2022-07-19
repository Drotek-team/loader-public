from typing import List

import numpy as np

from ...drones_manager.trajectory_simulation_manager.trajectory_simulation_manager import (
    PositionSimulation,
)
from ...parameter.parameter import TimecodeParameter
from .dance_simulation import DanceSequence
from .position_simulation import linear_interpolation


def flight_simulation(
    positions_simulation: List[PositionSimulation],
    timecode_parameter: TimecodeParameter,
) -> DanceSequence:
    flight_positions: List[np.ndarray] = []
    for position_simulation, next_positions_simulation in zip(
        positions_simulation[:-1], positions_simulation[1:]
    ):
        flight_positions += linear_interpolation(
            position_simulation.xyz,
            next_positions_simulation.xyz,
            int(
                ((next_positions_simulation.second - position_simulation.second))
                / timecode_parameter.position_second_rate
            ),
        )
    # flight_positions.append(
    #     json_convertion_constant.from_json_position_to_simulation_position(
    #         position_events[-1].get_values()
    #     )
    # )
    return DanceSequence(
        flight_positions, len(flight_positions) * [True], len(flight_positions) * [True]
    )
