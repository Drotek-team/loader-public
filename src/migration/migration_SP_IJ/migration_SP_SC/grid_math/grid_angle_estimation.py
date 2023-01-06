import math
from typing import Tuple

import numpy as np

from .grid import Grid, HorizontalPosition


def get_first_row_extremes(
    grid: Grid,
) -> Tuple[HorizontalPosition, HorizontalPosition]:

    extreme_horizontal_positions = list(grid.horizontal_x_extremes) + list(
        grid.horizontal_y_extremes
    )
    sorted_extreme_horizontal_positions = sorted(
        extreme_horizontal_positions,
        key=lambda extreme_horizontal_position: extreme_horizontal_position.drone_index,
    )
    return (
        sorted_extreme_horizontal_positions[0],
        sorted_extreme_horizontal_positions[1],
    )


def get_angle_degree_from_vector(u_x: np.ndarray) -> int:
    u_x_unit = u_x / np.linalg.norm(u_x)
    angle_radian = np.arctan2(u_x_unit[1], u_x_unit[0])
    return int(math.degrees(angle_radian))


def get_angle_takeoff_from_grid(
    grid: Grid,
) -> float:
    if len(grid) == 1:
        return 0.0
    (
        first_row_first_horizonal_position,
        first_row_last_horizonal_position,
    ) = get_first_row_extremes(grid)
    return get_angle_degree_from_vector(
        first_row_last_horizonal_position.xy_array
        - first_row_first_horizonal_position.xy_array
    )
