from typing import List, Tuple

import numpy as np

from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from .position_simulation import SimulationInfo, linear_interpolation


def generate_takeoff_first_part(
    takeoff_start_position: Tuple[float, float, float],
) -> List[np.ndarray]:
    takeoff_end_position = (
        takeoff_start_position[0],
        takeoff_start_position[1],
        takeoff_start_position[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter,
    )
    return linear_interpolation(
        takeoff_start_position,
        takeoff_end_position,
        int(
            TAKEOFF_PARAMETER.takeoff_elevation_duration_second
            * FRAME_PARAMETER.position_fps
        ),
    )


def generate_takeoff_second_part(
    takeoff_start_position: Tuple[float, float, float],
) -> List[np.ndarray]:
    takeoff_end_position = (
        takeoff_start_position[0],
        takeoff_start_position[1],
        takeoff_start_position[2] + TAKEOFF_PARAMETER.takeoff_altitude_meter,
    )
    return linear_interpolation(
        takeoff_end_position,
        takeoff_end_position,
        int(
            TAKEOFF_PARAMETER.takeoff_stabilisation_duration_second
            * FRAME_PARAMETER.position_fps
        )
        - 1,
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
    takeoff_simulation = [
        SimulationInfo(frame_begin + frame_index, takeoff_position, True, False)
        for frame_index, takeoff_position in enumerate(takeoff_positions)
    ]
    return takeoff_simulation
