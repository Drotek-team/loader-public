from typing import List

import numpy as np

from ....show_simulation.drone_simulation import PositionEventSimulation
from ....parameter.parameter import FrameParameter
from ....show_simulation.trajectory_simulation import (
    TrajectorySimulation,
)
from .position_simulation import linear_interpolation


from ....parameter.parameter import (
    FrameParameter,
)


def flight_simulation(
    position_events_simulation: List[PositionEventSimulation],
    frame_parameter: FrameParameter,
) -> TrajectorySimulation:
    flight_positions: List[np.ndarray] = []
    for position_simulation, next_position_events_simulation in zip(
        position_events_simulation[:-1], position_events_simulation[1:]
    ):
        flight_positions += linear_interpolation(
            position_simulation.xyz,
            next_position_events_simulation.xyz,
            int(
                (next_position_events_simulation.frame - position_simulation.frame)
                // frame_parameter.position_rate_frame
            ),
        )
    return TrajectorySimulation(
        flight_positions,
        [True for _ in range(len(flight_positions))],
        [True for _ in range(len(flight_positions))],
    )
