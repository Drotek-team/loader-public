import math
from typing import Tuple

import numpy as np

from .grid import Grid, HorizontalPosition


def is_grid_a_row(grid: Grid) -> bool:
    return set(grid.horizontal_x_extremes) == set(grid.horizontal_y_extremes)


def get_angle_degree_from_vector(u_x: np.ndarray) -> int:
    u_x_unit = u_x / np.linalg.norm(u_x)
    angle_radian = np.arctan2(u_x_unit[1], u_x_unit[0])
    return int(math.degrees(angle_radian))


def get_first_row_extremes(
    grid: Grid,
) -> Tuple[HorizontalPosition, HorizontalPosition]:
    extreme_positions = list(grid.horizontal_x_extremes) + list(
        grid.horizontal_y_extremes
    )
    sorted_extreme_positions = sorted(
        extreme_positions,
        key=lambda extreme_position: extreme_position.drone_index,
    )
    if is_grid_a_row(grid):
        return (sorted_extreme_positions[0], sorted_extreme_positions[-1])
    return (
        sorted_extreme_positions[0],
        sorted_extreme_positions[1],
    )


def get_angle_takeoff_from_grid(
    grid: Grid,
) -> float:
    if len(grid) == 1:
        return 0.0
    (
        first_row_first_position,
        first_row_last_position,
    ) = get_first_row_extremes(grid)
    return get_angle_degree_from_vector(
        first_row_last_position.xy_array - first_row_first_position.xy_array
    )


def get_ned_angle_takeoff_from_grid(grid: Grid) -> float:
    angle = get_angle_takeoff_from_grid(grid)
    return angle - 90 if angle != 0.0 else angle
