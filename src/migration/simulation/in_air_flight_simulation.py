from typing import List

import numpy as np

from ...show_user.show_user import PositionEventUser
from .position_simulation import SimulationInfo, linear_interpolation


def in_air_flight_simulation(
    position_events_user: List[PositionEventUser],
) -> List[SimulationInfo]:
    flight_positions: List[np.ndarray] = []
    for position_simulation, next_position_events_user in zip(
        position_events_user[:-1], position_events_user[1:]
    ):
        flight_positions += linear_interpolation(
            position_simulation.xyz,
            next_position_events_user.xyz,
            next_position_events_user.frame - position_simulation.frame,
        )
    flight_positions.append(np.array(position_events_user[-1].xyz))
    return [
        SimulationInfo(
            frame=position_events_user[0].frame - 1 + frame_index,
            position=flight_position,
            in_air=True,
            in_dance=True,
        )
        for frame_index, flight_position in enumerate(flight_positions)
    ]
