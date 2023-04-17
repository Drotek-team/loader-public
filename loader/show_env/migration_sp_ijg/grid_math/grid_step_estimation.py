import numpy as np

from .grid import Grid


def get_step_from_grid(
    grid: Grid,
) -> float:
    for first_horizontal_position, second_horizontal_position in zip(
        grid[:-1],
        grid[1:],
    ):
        if first_horizontal_position.xy_tuple != second_horizontal_position.xy_tuple:
            return float(
                np.linalg.norm(
                    first_horizontal_position.xy_array - second_horizontal_position.xy_array,
                ),
            )
    return 0.0
