from typing import List, Tuple
import numpy as np
from ...parameter.parameter import LandParameter, FrameParameter
from ...show_trajectory.show_trajectory import (
    TrajectoryInfo,
)
from .position_simulation import linear_interpolation


def generate_land_first_part(
    land_start_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
    land_parameter: LandParameter,
) -> List[np.ndarray]:
    land_middle_position = (
        land_start_position[0],
        land_start_position[1],
        land_parameter.get_second_land_altitude_start(land_start_position[2]),
    )
    nb_iteration = int(
        land_parameter.get_first_land_second_delta(land_start_position[2])
        * frame_parameter.position_fps
    )
    return linear_interpolation(
        land_start_position,
        land_middle_position,
        nb_iteration,
    )


def generate_land_second_part(
    land_start_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
    land_parameter: LandParameter,
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
        int(
            land_parameter.get_second_land_second_delta(land_start_position[2])
            * frame_parameter.position_fps
        ),
    )


def land_simulation(
    land_start_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
    land_parameter: LandParameter,
) -> List[TrajectoryInfo]:
    land_positions = generate_land_first_part(
        land_start_position,
        frame_parameter,
        land_parameter,
    ) + generate_land_second_part(
        land_start_position,
        frame_parameter,
        land_parameter,
    )
    return [
        TrajectoryInfo(land_position, True, False) for land_position in land_positions
    ]
