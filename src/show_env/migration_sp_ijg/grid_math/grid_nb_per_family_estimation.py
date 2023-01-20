from .grid import Grid


def get_nb_drone_per_family_from_grid(
    grid: Grid,
) -> int:
    if grid.is_grid_one_family():
        return len(grid)

    for first_horizontal_position, second_horizontal_position in zip(
        grid[:-1],
        grid[1:],
    ):
        if first_horizontal_position.xy_tuple != second_horizontal_position.xy_tuple:
            return second_horizontal_position.drone_index
    msg = f"Grid is not valid: {grid}"
    raise ValueError(msg)
