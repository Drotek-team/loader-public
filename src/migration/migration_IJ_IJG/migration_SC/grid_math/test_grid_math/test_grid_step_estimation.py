import pytest
from ..grid import Grid
from ..grid_step_estimation import get_step_from_grid


@pytest.fixture
def valid_grid():
    return Grid([(-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0), (1.0, 1.0)])


@pytest.fixture
def valid_grid_step_two_meter():
    return Grid([(-2.0, -2.0), (2.0, -2.0), (-2.0, 2.0), (2.0, 2.0)])


def test_get_nb_drone_per_family_from_grid_valid_grid(valid_grid: Grid):
    assert get_step_from_grid(valid_grid) == 2.0


def test_get_nb_drone_per_family_from_grid_valid_grid_step_two_metery(
    valid_grid_step_two_meter: Grid,
):
    assert get_step_from_grid(valid_grid_step_two_meter) == 4.0
