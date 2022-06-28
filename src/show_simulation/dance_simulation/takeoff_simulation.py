from typing import List

import numpy as np

from ...parameter.parameter import TakeoffParameter, TimecodeParameter
from .position_simulation import linear_interpolation, truncated_integer


def generate_first_part_takeoff(
    takeoff_start_timecode: int,
    takeoff_start_position: np.ndarray,
    takeoff_end_position: np.ndarray,
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
) -> List[np.ndarray]:
    truncated_takeoff_start_timecode = truncated_integer(
        takeoff_start_timecode,
        timecode_parameter.position_timecode_rate,
    )
    takeoff_first_part_frames = list(
        np.arange(
            truncated_takeoff_start_timecode,
            truncated_takeoff_start_timecode
            + takeoff_parameter.takeoff_elevation_duration,
            timecode_parameter.position_timecode_rate,
        )
    )
    return linear_interpolation(
        takeoff_start_position,
        takeoff_end_position,
        takeoff_first_part_frames / takeoff_parameter.takeoff_elevation_duration,
    )


def generate_takeoff_second_part(
    takeoff_start_timecode: int,
    takeoff_end_timecode: int,
    takeoff_end_position: np.ndarray,
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
) -> List[np.ndarray]:
    truncated_takeoff_second_part_start_frame = truncated_integer(
        takeoff_start_timecode + takeoff_parameter.takeoff_stabilisation_duration,
        timecode_parameter.position_timecode_rate,
    )
    takeoff_second_part_frames = list(
        np.arange(
            truncated_takeoff_second_part_start_frame,
            takeoff_end_timecode,
            timecode_parameter.position_timecode_rate,
        )
    )
    return len(takeoff_second_part_frames) * [takeoff_end_position]


def takeoff_simulation(
    takeoff_start_timecode: int,
    takeoff_end_timecode: int,
    takeoff_start_position: np.ndarray,
    takeoff_end_position: np.ndarray,
    timecode_parameter: TimecodeParameter,
    takeoff_parameter: TakeoffParameter,
):
    return generate_first_part_takeoff(
        takeoff_start_timecode,
        takeoff_start_position,
        takeoff_end_position,
        timecode_parameter,
        takeoff_parameter,
    ) + generate_takeoff_second_part(
        takeoff_start_timecode,
        takeoff_end_timecode,
        takeoff_end_position,
        timecode_parameter,
        takeoff_parameter,
    )
