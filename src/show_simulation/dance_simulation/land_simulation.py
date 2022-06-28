from typing import List

import numpy as np

from ...parameter.parameter import LandParameter, TimecodeParameter
from .position_simulation import linear_interpolation, truncated_integer


def generate_land_first_part(
    land_start_position: np.ndarray,
    land_start_timecode: int,
    land_parameter: LandParameter,
    timecode_parameter: TimecodeParameter,
) -> List[np.ndarray]:
    truncated_first_land_start_timecode = truncated_integer(
        land_start_timecode,
        timecode_parameter.position_timecode_rate,
    )
    land_first_part_frames = list(
        np.arange(
            truncated_first_land_start_timecode,
            land_parameter.get_first_land_frame_delta(),
            timecode_parameter.position_timecode_rate,
        )
    )
    return linear_interpolation(
        land_start_position,
        np.array(
            [
                land_start_position[0],
                land_start_position[1],
                land_parameter.get_first_land_altitude(land_start_position[2]),
            ]
        ),
        land_first_part_frames / land_parameter.get_first_land_frame_delta(),
    )


def generate_land_second_part(
    land_start_timecode: int,
    land_parameter: LandParameter,
    timecode_parameter: TimecodeParameter,
) -> List[np.ndarray]:
    truncated_second_land_start_timecode = truncated_integer(
        land_start_timecode + land_parameter.get_first_land_frame_delta(),
        timecode_parameter.position_timecode_rate,
    )
    land_second_part_frames = list(
        np.arange(
            truncated_second_land_start_timecode,
            land_parameter.get_second_land_frame_delta(),
            timecode_parameter.position_timecode_rate,
        )
    )
    return linear_interpolation(
        land_parameter.get_second_land_altitude_start(),
        0,
        land_second_part_frames / land_parameter.get_second_land_frame_delta(),
    )


def generate_land_third_part(
    land_start_timecode: int,
    land_parameter: LandParameter,
    timecode_parameter: TimecodeParameter,
) -> List[np.ndarray]:
    truncated_second_land_start_timecode = truncated_integer(
        land_start_timecode + land_parameter.get_first_land_frame_delta(),
        timecode_parameter.position_timecode_rate,
    )
    land_second_part_frames = list(
        np.arange(
            truncated_second_land_start_timecode,
            land_parameter.get_second_land_frame_delta(),
            timecode_parameter.position_timecode_rate,
        )
    )
    return linear_interpolation(
        land_parameter.get_second_land_altitude_start(),
        0,
        land_second_part_frames / land_parameter.get_second_land_frame_delta(),
    )


def land_simulation(
    land_start_timecode: int,
    land_start_position: np.ndarray,
    land_parameter: LandParameter,
    timecode_parameter: TimecodeParameter,
) -> List[np.ndarray]:
    return [
        generate_land_first_part(
            land_start_position, land_start_timecode, land_parameter, timecode_parameter
        )
        + generate_land_second_part(
            land_start_timecode, land_parameter, timecode_parameter
        )
        + generate_land_third_part(
            land_start_timecode, land_parameter, timecode_parameter
        )
    ]
