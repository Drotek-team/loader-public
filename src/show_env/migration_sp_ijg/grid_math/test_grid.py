import numpy as np

from .grid import Coordinate, Grid, HorizontalPosition


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


def test_is_grid_one_drone():
    first_horizontal_position = HorizontalPosition(0, Coordinate(-1.0, -1.0))
    second_horizontal_position = HorizontalPosition(1, Coordinate(1.0, -1.0))
    third_horizontal_position = HorizontalPosition(2, Coordinate(-1.0, 1.0))
    fourth_horizontal_position = HorizontalPosition(3, Coordinate(1.0, 1.0))
    grid = Grid(
        [
            first_horizontal_position,
            second_horizontal_position,
            third_horizontal_position,
            fourth_horizontal_position,
        ]
    )
    assert not grid.is_grid_one_drone()

    grid = Grid([first_horizontal_position])
    assert grid.is_grid_one_drone()


# TODO: finish this test
def test_grid_standard_case_and_method():
    first_horizontal_position = HorizontalPosition(0, Coordinate(-1.0, -1.0))
    second_horizontal_position = HorizontalPosition(1, Coordinate(1.0, -1.0))
    third_horizontal_position = HorizontalPosition(2, Coordinate(-1.0, 1.0))
    fourth_horizontal_position = HorizontalPosition(3, Coordinate(1.0, 1.0))
    grid = Grid(
        [
            first_horizontal_position,
            second_horizontal_position,
            third_horizontal_position,
            fourth_horizontal_position,
        ]
    )
    assert grid
