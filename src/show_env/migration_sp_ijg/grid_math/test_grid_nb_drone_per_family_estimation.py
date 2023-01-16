import pytest

from .grid import Grid, get_grid_from_horizontal_positions
from .grid_nb_per_family_estimation import get_nb_drone_per_family_from_grid


@pytest.fixture
def valid_grid():
    return get_grid_from_horizontal_positions(
        [(-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0), (1.0, 1.0)]
    )


@pytest.fixture
def valid_grid_two_drone_per_family():
    return get_grid_from_horizontal_positions(
        [
            (-1.0, -1.0),
            (-1.0, -1.0),
            (1.0, -1.0),
            (1.0, -1.0),
            (-1.0, 1.0),
            (-1.0, 1.0),
            (1.0, 1.0),
            (1.0, 1.0),
        ]
    )


def test_get_nb_drone_per_family_from_grid_valid_grid(valid_grid: Grid):
    assert get_nb_drone_per_family_from_grid(valid_grid) == 1


def test_get_nb_drone_per_family_from_grid_valid_grid_two_drone_per_family(
    valid_grid_two_drone_per_family: Grid,
):
    assert get_nb_drone_per_family_from_grid(valid_grid_two_drone_per_family) == 2
    assert get_nb_drone_per_family_from_grid(valid_grid_two_drone_per_family) == 2
