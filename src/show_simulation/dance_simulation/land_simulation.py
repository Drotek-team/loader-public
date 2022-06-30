from typing import List, Tuple

import numpy as np

from ...parameter.parameter import (
    JsonConventionConstant,
    LandParameter,
    TimecodeParameter,
)
from .dance_simulation import DanceSequence
from .position_simulation import linear_interpolation


def generate_land_first_part(
    land_start_position: Tuple[int, int, int],
    timecode_parameter: TimecodeParameter,
    land_parameter: LandParameter,
    json_convention_constant: JsonConventionConstant,
) -> List[np.ndarray]:
    land_middle_position = (
        land_start_position[0],
        land_start_position[1],
        land_parameter.get_second_land_altitude_start(land_start_position[2]),
    )
    nb_iteration = (
        land_parameter.get_first_land_timecode_delta(land_start_position[2])
        // timecode_parameter.position_timecode_rate
    )
    return linear_interpolation(
        land_start_position,
        land_middle_position,
        nb_iteration,
        json_convention_constant,
    )


def generate_land_second_part(
    land_start_position: Tuple[int, int, int],
    timecode_parameter: TimecodeParameter,
    land_parameter: LandParameter,
    json_convention_constant: JsonConventionConstant,
) -> List[np.ndarray]:
    land_middle_position = (
        land_start_position[0],
        land_start_position[1],
        land_parameter.get_second_land_altitude_start(land_start_position[2]),
    )
    land_end_position = (
        land_start_position[0],
        land_start_position[1],
        0,
    )
    return linear_interpolation(
        land_middle_position,
        land_end_position,
        land_parameter.get_second_land_timecode_delta(land_start_position[2])
        // timecode_parameter.position_timecode_rate,
        json_convention_constant,
    )


def land_simulation(
    land_start_position: Tuple[int, int, int],
    timecode_parameter: TimecodeParameter,
    land_parameter: LandParameter,
    json_convention_constant: JsonConventionConstant,
) -> DanceSequence:
    land_positions = generate_land_first_part(
        land_start_position,
        timecode_parameter,
        land_parameter,
        json_convention_constant,
    )
    # + generate_land_second_part(
    #     land_start_position,
    #     timecode_parameter,
    #     land_parameter,
    #     json_convention_constant,
    # )
    return DanceSequence(
        land_positions, len(land_positions) * [True], len(land_positions) * [False]
    )
