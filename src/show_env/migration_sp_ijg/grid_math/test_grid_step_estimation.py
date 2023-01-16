import pytest

from .grid import Grid, get_grid_from_horizontal_positions
from .grid_step_estimation import get_step_from_grid


@pytest.fixture
def valid_grid():
    return get_grid_from_horizontal_positions(
        [(-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0), (1.0, 1.0)]
    )


@pytest.fixture
def valid_grid_step_two_meter():
    return get_grid_from_horizontal_positions(
        [(-2.0, -2.0), (2.0, -2.0), (-2.0, 2.0), (2.0, 2.0)]
    )


def test_get_nb_drone_per_family_from_grid_valid_grid(valid_grid: Grid):
    assert get_step_from_grid(valid_grid) == 2.0


def test_get_nb_drone_per_family_from_grid_valid_grid_step_two_metery(
    valid_grid_step_two_meter: Grid,
):
    assert get_step_from_grid(valid_grid_step_two_meter) == 4.0
    assert get_step_from_grid(valid_grid_step_two_meter) == 4.0
