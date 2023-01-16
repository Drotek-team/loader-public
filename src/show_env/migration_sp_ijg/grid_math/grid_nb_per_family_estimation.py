from .grid import Grid


def get_nb_drone_per_family_from_grid(
    grid: Grid,
) -> int:
    horizontal_position_index_0 = grid[0]

    # One family Exception
    if all(
        horizontal_position == horizontal_position_index_0
        for horizontal_position in grid
    ):
        return len(grid)

    # General algorithm
    for first_horizontal_position, second_horizontal_position in zip(
        grid[:-1],
        grid[1:],
    ):
        if first_horizontal_position.xy_tuple != second_horizontal_position.xy_tuple:
            return second_horizontal_position.drone_index
    return 0
