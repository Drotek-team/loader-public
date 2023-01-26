import numpy as np

from ....show_env.show_user.generate_show_user import GridConfiguration
from ...show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user
from .grid import (
    Coordinate,
    HorizontalPosition,
    get_grid_from_configuration,
    get_grid_from_show_user,
)


def test_coordinate_standard_case_and_method():
    coordinate = Coordinate(1.0, 2.0)
    assert np.array_equal(coordinate.xy_array, np.array([1.0, 2.0]))
    assert coordinate.xy_tuple == (1.0, 2.0)


def test_horizontal_position_standard_case_and_method():
    first_horizontal_position = HorizontalPosition(1, Coordinate(-1.0, 1.0))
    assert first_horizontal_position.x == -1.0
    assert first_horizontal_position.y == 1.0
    assert np.array_equal(first_horizontal_position.xy_array, np.array([-1.0, 1.0]))
    assert first_horizontal_position.xy_tuple == (-1.0, 1.0)

    first_horizontal_position.rotated_positions(0.0)
    assert first_horizontal_position.coordinate == Coordinate(-1.0, 1.0)

    first_horizontal_position.rotated_positions(np.pi)
    assert (
        np.linalg.norm(first_horizontal_position.xy_array - np.array([1.0, -1.0]))
        < 1e-6
    )


def test_grid_is_grid_one_drone():
    grid = get_grid_from_configuration(GridConfiguration())
    assert grid.is_grid_one_drone()
    grid = get_grid_from_configuration(GridConfiguration(nb_x=2))
    assert not grid.is_grid_one_drone()


def test_grid_is_grid_one_family():
    grid = get_grid_from_configuration(GridConfiguration(nb_drone_per_family=2))
    assert grid.is_grid_one_family()
    grid = get_grid_from_configuration(GridConfiguration(nb_x=2))
    assert not grid.is_grid_one_family()


def test_grid_rotate_horizontal_positions():
    grid = get_grid_from_configuration(GridConfiguration(nb_x=2, nb_y=2, step=2.0))
    grid.rotate_horizontal_positions(0.0)
    assert grid[0].coordinate == Coordinate(-1.0, -1.0)
    grid.rotate_horizontal_positions(np.pi)
    assert grid[0].coordinate == Coordinate(1.0, 1.0)
    grid.rotate_horizontal_positions(-np.pi)
    assert grid[0].coordinate == Coordinate(-1.0, -1.0)


def test_get_grid_from_show_user():
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2, step=2.0))
    grid = get_grid_from_show_user(show_user)
    assert grid[0].coordinate == Coordinate(-1.0, -1.0)
    assert grid[1].coordinate == Coordinate(1.0, -1.0)
    assert grid[2].coordinate == Coordinate(-1.0, 1.0)
    assert grid[3].coordinate == Coordinate(1.0, 1.0)


def test_get_grid_from_show_configuration():
    grid = get_grid_from_configuration(GridConfiguration(nb_x=2, nb_y=2, step=2.0))
    assert grid[0].coordinate == Coordinate(-1.0, -1.0)
    assert grid[1].coordinate == Coordinate(1.0, -1.0)
    assert grid[2].coordinate == Coordinate(-1.0, 1.0)
    assert grid[3].coordinate == Coordinate(1.0, 1.0)
