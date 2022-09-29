from typing import List, Tuple

import numpy as np

from ....parameter.parameter import TakeoffParameter, FrameParameter
from ....show_simulation.trajectory_simulation import (
    TrajectorySimulation,
)
from .position_simulation import linear_interpolation


def generate_takeoff_first_part(
    takeoff_start_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
) -> List[np.ndarray]:
    takeoff_end_position = (
        takeoff_start_position[0],
        takeoff_start_position[1],
        takeoff_start_position[2] + takeoff_parameter.takeoff_altitude_meter,
    )
    return linear_interpolation(
        takeoff_start_position,
        takeoff_end_position,
        int(
            takeoff_parameter.takeoff_elevation_duration_second
            * frame_parameter.position_fps
        ),
    )


def generate_takeoff_second_part(
    takeoff_start_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
) -> List[np.ndarray]:
    takeoff_end_position = (
        takeoff_start_position[0],
        takeoff_start_position[1],
        takeoff_start_position[2] + takeoff_parameter.takeoff_altitude_meter,
    )
    return int(
        takeoff_parameter.takeoff_stabilisation_duration_second
        * frame_parameter.position_fps
    ) * [np.array(takeoff_end_position)]


def takeoff_simulation(
    takeoff_start_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
    takeoff_parameter: TakeoffParameter,
) -> TrajectorySimulation:
    takeoff_positions = generate_takeoff_first_part(
        takeoff_start_position,
        frame_parameter,
        takeoff_parameter,
    ) + generate_takeoff_second_part(
        takeoff_start_position,
        frame_parameter,
        takeoff_parameter,
    )
    return TrajectorySimulation(
        takeoff_positions,
        len(takeoff_positions) * [True],
        len(takeoff_positions) * [False],
    )
