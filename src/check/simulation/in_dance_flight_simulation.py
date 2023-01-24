from typing import List

import numpy as np
import numpy.typing as npt

from ...show_env.show_user.show_user import PositionEventUser
from .position_simulation import SimulationInfo, linear_interpolation


def in_dance_flight_simulation(
    position_events_user: List[PositionEventUser],
) -> List[SimulationInfo]:
    flight_positions: List[npt.NDArray[np.float64]] = []
    for position_simulation, next_position_events_user in zip(
        position_events_user[:-1], position_events_user[1:]
    ):
        flight_positions += linear_interpolation(
            position_simulation.xyz,
            next_position_events_user.xyz,
            next_position_events_user.frame - position_simulation.frame,
        )
    return [
        SimulationInfo(
            frame=position_events_user[0].frame + frame_index,
            position=flight_position,
            in_air=True,
        )
        for frame_index, flight_position in enumerate(flight_positions)
    ]
