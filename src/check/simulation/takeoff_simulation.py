from typing import List, Tuple

import numpy as np
import numpy.typing as npt

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from .position_simulation import SimulationInfo, linear_interpolation


def generate_takeoff_first_part(
    takeoff_start_position: Tuple[float, float, float],
) -> List[npt.NDArray[np.float64]]:
    takeoff_end_position = (
        takeoff_start_position[0],
        takeoff_start_position[1],
        takeoff_start_position[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
    )
    return linear_interpolation(
        takeoff_start_position,
        takeoff_end_position,
        FRAME_PARAMETER.from_second_to_frame(
            TAKEOFF_PARAMETER.takeoff_elevation_duration_second
        ),
    )


def generate_takeoff_second_part(
    takeoff_start_position: Tuple[float, float, float],
) -> List[npt.NDArray[np.float64]]:
    takeoff_end_position = (
        takeoff_start_position[0],
        takeoff_start_position[1],
        takeoff_start_position[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
    )
    return linear_interpolation(
        takeoff_end_position,
        takeoff_end_position,
        FRAME_PARAMETER.from_second_to_frame(
            TAKEOFF_PARAMETER.takeoff_stabilisation_duration_second
        ),
    )


def takeoff_simulation(
    takeoff_start_position: Tuple[float, float, float],
    frame_begin: int,
) -> List[SimulationInfo]:
    takeoff_positions = generate_takeoff_first_part(
        takeoff_start_position,
    ) + generate_takeoff_second_part(
        takeoff_start_position,
    )
    return [
        SimulationInfo(
            frame=frame_begin + frame_index,
            position=takeoff_position,
            in_air=True,
        )
        for frame_index, takeoff_position in enumerate(takeoff_positions)
    ]
