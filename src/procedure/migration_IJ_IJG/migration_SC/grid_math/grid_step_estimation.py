from .grid import Grid
import numpy as np


def get_step_from_grid(
    grid: Grid,
) -> float:
    first_horizontal_position_index_0 = grid[0]
    if all(
        np.array_equal(
            first_horizontal_position.xy_array,
            first_horizontal_position_index_0.xy_array,
        )
        for first_horizontal_position in grid
    ):
        return 0
    for first_horizontal_position, second_horizontal_position in zip(
        grid.horizontal_positions[:-1], grid.horizontal_positions[1:]
    ):
        if (first_horizontal_position.xy_tuple != second_horizontal_position.xy_tuple,):
            return np.linalg.norm(
                first_horizontal_position.xy_array
                - second_horizontal_position.xy_array,
            )
    return 0.0
