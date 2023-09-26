from typing import TYPE_CHECKING, List, Tuple

from loader.parameters import FRAME_PARAMETERS, LAND_PARAMETERS

from .position_simulation import SimulationInfo, linear_interpolation

if TYPE_CHECKING:
    import numpy as np
    from numpy.typing import NDArray


def generate_land_first_part(
    land_start_position: Tuple[float, float, float],
) -> List["NDArray[np.float64]"]:
    land_middle_position = (
        land_start_position[0],
        land_start_position[1],
        LAND_PARAMETERS.get_second_land_altitude_start(land_start_position[2]),
    )
    return linear_interpolation(
        land_start_position,
        land_middle_position,
        FRAME_PARAMETERS.from_second_to_frame(
            LAND_PARAMETERS.get_first_land_second_delta(land_start_position[2]),
        ),
    )


def generate_land_second_part(
    land_start_position: Tuple[float, float, float],
) -> List["NDArray[np.float64]"]:
    land_middle_position = (
        land_start_position[0],
        land_start_position[1],
        LAND_PARAMETERS.get_second_land_altitude_start(land_start_position[2]),
    )
    land_end_position = (
        land_start_position[0],
        land_start_position[1],
        0,
    )
    return linear_interpolation(
        land_middle_position,
        land_end_position,
        FRAME_PARAMETERS.from_second_to_frame(
            LAND_PARAMETERS.get_second_land_second_delta(land_start_position[2]),
        ),
    )


def land_simulation(
    land_start_position: Tuple[float, float, float],
    frame_begin: int,
) -> List["SimulationInfo"]:
    land_positions = generate_land_first_part(
        land_start_position,
    ) + generate_land_second_part(
        land_start_position,
    )
    return [
        SimulationInfo(
            frame=frame_begin + frame_index,
            position=land_position,
        )
        for frame_index, land_position in enumerate(land_positions)
    ]
