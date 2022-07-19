from typing import List, Tuple

import numpy as np

from ...parameter.parameter import TakeoffParameter, TimecodeParameter
from .dance_simulation import DanceSequence
from .position_simulation import linear_interpolation


def generate_takeoff_first_part(
    takeoff_start_position: Tuple[float, float, float],
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
) -> List[np.ndarray]:
    takeoff_end_position = (
        takeoff_start_position[0],
        takeoff_start_position[1],
        takeoff_start_position[2] + takeoff_parameter.takeoff_simulation_altitude,
    )
    return linear_interpolation(
        takeoff_start_position,
        takeoff_end_position,
        int(
            takeoff_parameter.takeoff_elevation_simulation_duration
            / timecode_parameter.position_second_rate
        ),
    )


def generate_takeoff_second_part(
    takeoff_start_position: Tuple[float, float, float],
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
) -> List[np.ndarray]:
    takeoff_end_position = (
        takeoff_start_position[0],
        takeoff_start_position[1],
        takeoff_start_position[2] + takeoff_parameter.takeoff_simulation_altitude,
    )
    return int(
        takeoff_parameter.takeoff_stabilisation_simulation_duration
        / timecode_parameter.position_second_rate
    ) * [np.array(takeoff_end_position)]


def takeoff_simulation(
    takeoff_start_position: Tuple[float, float, float],
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
) -> DanceSequence:
    takeoff_positions = generate_takeoff_first_part(
        takeoff_start_position,
        timecode_parameter,
        takeoff_parameter,
    ) + generate_takeoff_second_part(
        takeoff_start_position,
        timecode_parameter,
        takeoff_parameter,
    )
    return DanceSequence(
        takeoff_positions,
        len(takeoff_positions) * [True],
        len(takeoff_positions) * [False],
    )
