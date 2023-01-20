import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from .grid import (
    Coordinate,
    Grid,
    GridConfiguration,
    HorizontalPosition,
    get_grid_from_configuration,
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


@given(
    nb_x=st.integers(1, 1),
    nb_y=st.integers(2, 2),
    nb_drone_per_family=st.integers(2, 2),
    angle_takeoff=st.floats(1, np.pi),
)
def test_is_grid_a_row(
    nb_x: int, nb_y: int, nb_drone_per_family: int, angle_takeoff: float
):
    grid = get_grid_from_configuration(
        GridConfiguration(
            nb_x=nb_x,
            nb_y=nb_y,
            nb_drone_per_family=nb_drone_per_family,
            step_takeoff=1.5,
            angle_takeoff=angle_takeoff,
        )
    )
    assert grid.is_grid_a_row(nb_drone_per_family) == (nb_x == 1 or nb_y == 1)


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
    assert grid.horizontal_x_extremes(1) == (
        first_horizontal_position,
        fourth_horizontal_position,
    )
    assert grid.horizontal_y_extremes(1) == (
        first_horizontal_position,
        fourth_horizontal_position,
    )

    grid.rotate_horizontal_positions(0.0)
    assert grid.horizontal_x_extremes(1) == (
        first_horizontal_position,
        fourth_horizontal_position,
    )
    assert grid.horizontal_y_extremes(1) == (
        first_horizontal_position,
        fourth_horizontal_position,
    )

    grid.rotate_horizontal_positions(0.5 * np.pi)
    assert grid.horizontal_x_extremes(1) == (
        third_horizontal_position,
        second_horizontal_position,
    )
    assert grid.horizontal_y_extremes(1) == (
        first_horizontal_position,
        fourth_horizontal_position,
    )
