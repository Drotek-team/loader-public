from typing import Tuple

import numpy as np

from .grid import Grid

ARBITRARY_ROUNDING_TOLERANCE = 1e-6


def get_nb_x_nb_y_from_grid(
    grid: Grid,
    nb_drone_per_family: int,
    angle_radian: float,
) -> Tuple[int, int]:
    grid.rotate_horizontal_positions(-angle_radian)
    for first_horizontal_position, second_horizontal_position in zip(
        grid[:-1],
        grid[1:],
    ):
        if not np.allclose(
            first_horizontal_position.y,
            second_horizontal_position.y,
            rtol=ARBITRARY_ROUNDING_TOLERANCE,
        ):
            return (
                second_horizontal_position.drone_index // nb_drone_per_family,
                len(grid) // (second_horizontal_position.drone_index),
            )
    grid.rotate_horizontal_positions(angle_radian)
    return (len(grid) // nb_drone_per_family, 1)
