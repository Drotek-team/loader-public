import pytest

from .grid import Grid, get_grid_from_horizontal_positions
from .grid_nb_x_nb_y_estimation import get_nb_x_nb_y_from_grid


@pytest.fixture
def valid_grid():
    return get_grid_from_horizontal_positions(
        [(-1.0, -1.0), (-1.0, 1.0), (1.0, -1.0), (1.0, 1.0)]
    )


@pytest.fixture
def valid_grid_two_drones():
    return get_grid_from_horizontal_positions([(-1.0, 0.0), (1.0, 0.0)])


def test_get_nb_drone_per_family_from_grid_valid_grid(valid_grid: Grid):
    assert get_nb_x_nb_y_from_grid(valid_grid, 0) == (2, 2)


def test_get_nb_drone_per_family_from_grid_valid_grid_step_two_metery(
    valid_grid_two_drones: Grid,
):
    assert get_nb_x_nb_y_from_grid(valid_grid_two_drones, 0) == (1, 2)
    assert get_nb_x_nb_y_from_grid(valid_grid_two_drones, 0) == (1, 2)
