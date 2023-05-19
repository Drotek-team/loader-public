from .grid import Grid


def get_nb_drone_per_family_from_grid(
    grid: Grid,
) -> int:
    for first_horizontal_position, second_horizontal_position in zip(
        grid[:-1],
        grid[1:],
    ):
        if first_horizontal_position.xy_tuple != second_horizontal_position.xy_tuple:
            # Case where there are multiple families
            return second_horizontal_position.drone_index
    # Case where there is only one family
    return len(grid)
