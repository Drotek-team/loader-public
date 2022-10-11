from typing import Tuple
from .grid import Grid
import numpy as np


def get_nb_x_nb_y_from_grid(grid: Grid, grid_angle: float) -> Tuple[int, int]:
    ARBITRARY_ROUNDING_TOLERANCE = 1e-3
    grid.rotate_horizontal_positions(grid_angle)
    for first_horizontal_position, second_horizontal_position in zip(
        grid.horizontal_positions[:-1],
        grid.horizontal_positions[1:],
    ):
        if (
            np.abs(first_horizontal_position.y - second_horizontal_position.y)
            > ARBITRARY_ROUNDING_TOLERANCE
        ):
            return (
                second_horizontal_position.drone_index,
                len(grid) // second_horizontal_position.drone_index,
            )
    # Unique row corner case
    return len(grid), 1
