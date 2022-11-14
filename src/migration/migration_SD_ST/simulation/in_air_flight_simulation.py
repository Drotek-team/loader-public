from typing import List

import numpy as np

from ....show_dev.show_dev import PositionEventDev
from .position_simulation import SimulationInfo, linear_interpolation


def in_air_flight_simulation(
    position_events_dev: List[PositionEventDev],
) -> List[SimulationInfo]:
    flight_positions: List[np.ndarray] = []
    for position_simulation, next_position_events_dev in zip(
        position_events_dev[:-1], position_events_dev[1:]
    ):
        flight_positions += linear_interpolation(
            position_simulation.xyz,
            next_position_events_dev.xyz,
            (next_position_events_dev.frame - position_simulation.frame),
        )
    flight_positions.append(np.array(position_events_dev[-1].xyz))
    return [
        SimulationInfo(
            position_events_dev[0].frame + frame_index, flight_position, True, True
        )
        for frame_index, flight_position in enumerate(flight_positions)
    ]
