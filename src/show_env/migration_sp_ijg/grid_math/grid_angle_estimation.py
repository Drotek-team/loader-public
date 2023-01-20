from typing import Tuple

import numpy as np
import numpy.typing as npt

from .grid import Grid, HorizontalPosition


def get_angle_degree_from_vector(u_x: npt.NDArray[np.float64]) -> float:
    u_x_unit = u_x / np.linalg.norm(u_x)
    return np.arctan2(u_x_unit[1], u_x_unit[0])


def first_and_second_family_horizontal_positions(
    grid: Grid, nb_drone_per_family: int
) -> Tuple[HorizontalPosition, HorizontalPosition]:
    if grid.is_grid_one_drone() or grid.is_grid_one_family():
        return (grid[0], grid[0])
    return (grid[0], grid[nb_drone_per_family])


def get_angle_takeoff_from_grid(
    grid: Grid,
    nb_drone_per_family: int,
) -> float:
    if grid.is_grid_one_drone() or grid.is_grid_one_family():
        return 0.0
    (
        first_row_first_position,
        first_row_last_position,
    ) = first_and_second_family_horizontal_positions(grid, nb_drone_per_family)
    return get_angle_degree_from_vector(
        first_row_last_position.xy_array - first_row_first_position.xy_array
    )
