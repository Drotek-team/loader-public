from typing import List, Tuple

import numpy as np

from ...parameter.parameter import (
    JsonConventionConstant,
    TakeoffParameter,
    TimecodeParameter,
)
from .dance_simulation import DanceSequence
from .position_simulation import linear_interpolation


def generate_first_part_takeoff(
    takeoff_start_position: Tuple[int, int, int],
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
    json_convention_constant: JsonConventionConstant,
) -> List[np.ndarray]:
    takeoff_end_position = (
        takeoff_start_position[0],
        takeoff_start_position[1],
        takeoff_start_position[2] + takeoff_parameter.takeoff_altitude,
    )
    return linear_interpolation(
        takeoff_start_position,
        takeoff_end_position,
        takeoff_parameter.takeoff_elevation_duration
        // timecode_parameter.position_timecode_rate,
        json_convention_constant,
    )


def generate_takeoff_second_part(
    takeoff_start_position: Tuple[int, int, int],
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
    json_convention_constant: JsonConventionConstant,
) -> List[np.ndarray]:
    takeoff_end_position = (
        takeoff_start_position[0],
        takeoff_start_position[1],
        takeoff_start_position[2] + takeoff_parameter.takeoff_altitude,
    )
    return (
        takeoff_parameter.takeoff_stabilisation_duration
        // timecode_parameter.position_timecode_rate
    ) * [
        json_convention_constant.from_json_position_to_simulation_position(
            takeoff_end_position
        )
    ]


def takeoff_simulation(
    takeoff_start_position: Tuple[int, int, int],
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
    json_convention_constant: JsonConventionConstant,
) -> DanceSequence:
    takeoff_positions = generate_first_part_takeoff(
        takeoff_start_position,
        timecode_parameter,
        takeoff_parameter,
        json_convention_constant,
    ) + generate_takeoff_second_part(
        takeoff_start_position,
        timecode_parameter,
        takeoff_parameter,
        json_convention_constant,
    )
    return DanceSequence(
        takeoff_positions,
        len(takeoff_positions) * [True],
        len(takeoff_positions) * [False],
    )
