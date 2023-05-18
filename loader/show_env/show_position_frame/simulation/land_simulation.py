from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from loader.parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from loader.parameter.iostar_flight_parameter.iostar_land_parameter import LAND_PARAMETER

from .position_simulation import SimulationInfo, linear_interpolation

if TYPE_CHECKING:
    from numpy.typing import NDArray


def generate_land_first_part(
    land_start_position: tuple[float, float, float],
) -> list[NDArray[np.float64]]:
    land_middle_position = (
        land_start_position[0],
        land_start_position[1],
        LAND_PARAMETER.get_second_land_altitude_start(land_start_position[2]),
    )
    return linear_interpolation(
        land_start_position,
        land_middle_position,
        FRAME_PARAMETER.from_second_to_frame(
            LAND_PARAMETER.get_first_land_second_delta(land_start_position[2]),
        ),
    )


def generate_land_second_part(
    land_start_position: tuple[float, float, float],
) -> list[NDArray[np.float64]]:
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
        FRAME_PARAMETER.from_second_to_frame(
            LAND_PARAMETER.get_second_land_second_delta(land_start_position[2]),
        ),
    )


def land_simulation(
    land_start_position: tuple[float, float, float],
    frame_begin: int,
) -> list[SimulationInfo]:
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
        )
        for frame_index, land_position in enumerate(land_positions)
    ]
