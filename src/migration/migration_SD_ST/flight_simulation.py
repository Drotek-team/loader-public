from typing import List
import numpy as np
from ...parameter.parameter import FrameParameter
from ...show_trajectory.show_trajectory import (
    TrajectoryInfo,
)
from .position_simulation import (
    linear_interpolation,
    get_velocity_acceleration_from_positions,
)
from ...parameter.parameter import (
    FrameParameter,
)
from ...show_dev.show_dev import PositionEventDev


def flight_simulation(
    position_events_dev: List[PositionEventDev],
    frame_parameter: FrameParameter,
) -> List[TrajectoryInfo]:
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
    flight_velocities, flight_accelerations = get_velocity_acceleration_from_positions(
        flight_positions, frame_parameter.position_fps
    )
    return [
        TrajectoryInfo(
            flight_position, flight_velocity, flight_acceleration, True, True
        )
        for flight_position, flight_velocity, flight_acceleration in zip(
            flight_positions, flight_velocities, flight_accelerations
        )
    ]
