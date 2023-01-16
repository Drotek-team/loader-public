import numpy as np

from .grid import Grid


def get_step_from_grid(
    grid: Grid,
) -> int:
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
        grid[:-1], grid[1:]
    ):
        if first_horizontal_position.xy_tuple != second_horizontal_position.xy_tuple:
            return int(
                np.linalg.norm(
                    first_horizontal_position.xy_array
                    - second_horizontal_position.xy_array,
                )
            )
    return 0
