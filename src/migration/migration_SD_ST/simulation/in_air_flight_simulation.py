from typing import List
import numpy as np
from ....parameter.parameter import FrameParameter
from .position_simulation import linear_interpolation, SimulationInfo
from ....show_dev.show_dev import PositionEventDev


def in_air_flight_simulation(
    position_events_dev: List[PositionEventDev],
    frame_begin: int,
    frame_parameter: FrameParameter,
) -> List[SimulationInfo]:
    flight_positions: List[np.ndarray] = []
    for position_simulation, next_position_events_dev in zip(
        position_events_dev[:-1], position_events_dev[1:]
    ):
        ### TO DO: adapt that to new format
        flight_positions += linear_interpolation(
            position_simulation.xyz,
            next_position_events_dev.xyz,
            int(
                (next_position_events_dev.frame - position_simulation.frame)
                // frame_parameter.position_rate_frame
            ),
        )
    flight_positions.append(np.array(position_events_dev[-1].xyz))
    return [
        SimulationInfo(frame_begin + frame_index, flight_position, True, True)
        for frame_index, flight_position in enumerate(flight_positions)
    ]
