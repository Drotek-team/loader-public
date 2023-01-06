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
            (
                next_position_events_user.position_frame
                - position_simulation.position_frame
            ),
        )
    flight_positions.append(np.array(position_events_user[-1].xyz))
    return [
        SimulationInfo(
            position_events_user[0].position_frame - 1 + frame_index,
            flight_position,
            True,
            True,
        )
        for frame_index, flight_position in enumerate(flight_positions)
    ]
