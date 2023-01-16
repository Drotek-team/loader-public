import numpy as np
import pytest

from .grid import Grid
from .grid_angle_estimation import (
    get_angle_degree_from_vector,
    get_angle_takeoff_from_grid,
    get_first_row_extremes,
    is_grid_a_row,
)


@pytest.fixture
def valid_grid():
    return Grid([(-1.0, -1.0), (1.0, -1.0), (-1.0, 1.0), (1.0, 1.0)])


@pytest.fixture
def valid_grid_45_degree():
    return Grid([(2.0, 0.0), (0.0, 2.0), (-2.0, 0.0), (0.0, -2.0)])


@pytest.fixture
def valid_grid_90_degree():
    return Grid([(1.0, -1.0), (1.0, 1.0), (-1.0, 1.0), (-1.0, -1.0)])


@pytest.fixture
def one_point_grid():
    return Grid([(0.0, 0.0)])


@pytest.fixture
def horizontal_row_grid():
    return Grid([(0.0, 0.0), (1.0, 0.0)])


@pytest.fixture
def diagonal_row_grid():
    return Grid([(0.0, 0.0), (1.0, 1.0)])


@pytest.fixture
def vertical_row_grid():
    return Grid([(0.0, 0.0), (0.0, 1.0)])


def test_get_angle_from_vector():
    assert get_angle_degree_from_vector(np.array([1.0, 0])) == 0
    assert get_angle_degree_from_vector(np.array([-1.0, 0])) == 180
    assert get_angle_degree_from_vector(np.array([0, 1.0])) == 90
    assert get_angle_degree_from_vector(np.array([0, -1.0])) == -90
    assert get_angle_degree_from_vector(np.array([1.0, 1.0])) == 45
    assert get_angle_degree_from_vector(np.array([-1.0, -1.0])) == -135
    assert get_angle_degree_from_vector(np.array([-1.0, 1.0])) == 135
    assert get_angle_degree_from_vector(np.array([1.0, -1.0])) == -45


def test_is_grid_a_row_horizontal_row_grid(horizontal_row_grid: Grid):
    assert is_grid_a_row(horizontal_row_grid) is True


def test_is_grid_a_row_diagonal_row_grid(diagonal_row_grid: Grid):
    assert is_grid_a_row(diagonal_row_grid) is True


def test_is_grid_a_row_vertical_row_grid(vertical_row_grid: Grid):
    assert is_grid_a_row(vertical_row_grid) is True


def test_get_first_row_extremes(valid_grid: Grid):
    first_horizontal_position, second_horizontal_position = get_first_row_extremes(
        valid_grid
    )
    assert first_horizontal_position.drone_index == 0
    assert second_horizontal_position.drone_index == 1


def test_get_angle_takeoff_from_grid_valid_grid(valid_grid: Grid):
    assert get_angle_takeoff_from_grid(valid_grid) == 0


def test_get_angle_takeoff_from_grid_valid_grid_45_degree(valid_grid_45_degree: Grid):
    assert get_angle_takeoff_from_grid(valid_grid_45_degree) == 135


def test_get_angle_takeoff_from_grid_valid_grid_90_degree(valid_grid_90_degree: Grid):
    assert get_angle_takeoff_from_grid(valid_grid_90_degree) == 90


def test_get_angle_takeoff_from_grid_one_point_grid(one_point_grid: Grid):
    assert get_angle_takeoff_from_grid(one_point_grid) == 0.0
    assert get_angle_takeoff_from_grid(one_point_grid) == 0.0
