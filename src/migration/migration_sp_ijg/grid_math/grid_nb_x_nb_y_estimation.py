from typing import Tuple

import numpy as np

from .grid import Grid

ARBITRARY_ROUNDING_TOLERANCE = 1e-3


def get_nb_x_nb_y_from_grid(grid: Grid, grid_angle: float) -> Tuple[int, int]:
    grid.rotate_horizontal_positions(grid_angle)
    for first_horizontal_position, second_horizontal_position in zip(
        grid.horizontal_positions[:-1],
        grid.horizontal_positions[1:],
    ):
        if (
            np.abs(first_horizontal_position.x - second_horizontal_position.x)
            > ARBITRARY_ROUNDING_TOLERANCE
        ):
            return (
                second_horizontal_position.drone_index,
                len(grid) // second_horizontal_position.drone_index,
            )
    # Unique row corner case
    return len(grid), 1
