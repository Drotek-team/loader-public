from typing import List, Tuple

import numpy as np

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_land_parameter import LAND_PARAMETER
from .position_simulation import SimulationInfo, linear_interpolation


def generate_land_first_part(
    land_start_position: Tuple[float, float, float],
) -> List[np.ndarray]:
    land_middle_position = (
        land_start_position[0],
        land_start_position[1],
        LAND_PARAMETER.get_second_land_altitude_start(land_start_position[2]),
    )
    return linear_interpolation(
        land_start_position,
        land_middle_position,
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            LAND_PARAMETER.get_first_land_second_delta(land_start_position[2]),
        ),
    )


def generate_land_second_part(
    land_start_position: Tuple[float, float, float],
) -> List[np.ndarray]:
    land_middle_position = (
        land_start_position[0],
        land_start_position[1],
        LAND_PARAMETER.get_second_land_altitude_start(land_start_position[2]),
    )
    land_end_position = (
        land_start_position[0],
        land_start_position[1],
        0,
    )
    return linear_interpolation(
        land_middle_position,
        land_end_position,
        FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
            LAND_PARAMETER.get_second_land_second_delta(land_start_position[2])
        ),
    )


def land_simulation(
    land_start_position: Tuple[float, float, float],
    frame_begin: int,
) -> List[SimulationInfo]:
    land_positions = generate_land_first_part(
        land_start_position,
    ) + generate_land_second_part(
        land_start_position,
    )
    return [
        SimulationInfo(
            frame=frame_begin + frame_index,
            position=land_position,
            in_air=True,
            in_dance=False,
        )
        for frame_index, land_position in enumerate(land_positions)
    ]
