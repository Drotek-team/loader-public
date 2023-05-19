import math

import numpy as np
from hypothesis import given
from loader.shows.migrations.grid_math.grid import (
    GridConfiguration,
    get_grid_from_configuration,
)
from loader.shows.migrations.grid_math.grid_angle_estimation import (
    first_and_second_family_horizontal_positions,
    get_angle_degree_from_vector,
    get_angle_takeoff_from_grid,
)

from tests.strategies import (
    slow,
    st_angle_takeoff,
    st_nb_drone_per_family,
    st_nb_x,
    st_nb_y,
)


def test_get_angle_from_vector() -> None:
    assert get_angle_degree_from_vector(
        np.array([1.0, 0], dtype=np.float64),
    ) == math.radians(0)
    assert get_angle_degree_from_vector(
        np.array([0, 1.0], dtype=np.float64),
    ) == math.radians(90)
    assert get_angle_degree_from_vector(
        np.array([-1.0, 0], dtype=np.float64),
    ) == math.radians(180)
    assert get_angle_degree_from_vector(
        np.array([0, -1.0], dtype=np.float64),
    ) == math.radians(-90)
    assert get_angle_degree_from_vector(
        np.array([1.0, 1.0], dtype=np.float64),
    ) == math.radians(45)
    assert get_angle_degree_from_vector(
        np.array([-1.0, 1.0], dtype=np.float64),
    ) == math.radians(135)
    assert get_angle_degree_from_vector(
        np.array([-1.0, -1.0], dtype=np.float64),
    ) == math.radians(-135)
    assert get_angle_degree_from_vector(
        np.array([1.0, -1.0], dtype=np.float64),
    ) == math.radians(-45)


def test_first_and_second_family_horizontal_positions() -> None:
    nb_drone_per_family = 5
    one_drone_grid = get_grid_from_configuration(GridConfiguration())
    one_family_grid = get_grid_from_configuration(
        GridConfiguration(nb_drone_per_family=nb_drone_per_family),
    )
    standard_grid = get_grid_from_configuration(
        GridConfiguration(nb_x=2, nb_y=2, nb_drone_per_family=nb_drone_per_family),
    )
    assert first_and_second_family_horizontal_positions(one_drone_grid, 1) == (
        one_drone_grid[0],
        one_drone_grid[0],
    )
    assert first_and_second_family_horizontal_positions(
        one_family_grid,
        nb_drone_per_family,
    ) == (
        one_family_grid[0],
        one_family_grid[0],
    )
    assert first_and_second_family_horizontal_positions(
        standard_grid,
        nb_drone_per_family,
    ) == (
        standard_grid[0],
        standard_grid[nb_drone_per_family],
    )


# https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point
def angle_distance(first_angle_radian: float, second_angle_radian: float) -> float:
    first_angle, second_angle = math.degrees(first_angle_radian), math.degrees(
        second_angle_radian,
    )
    return abs((second_angle - first_angle + 180) % 360 - 180)


@given(
    nb_x=st_nb_x,
    nb_y=st_nb_y,
    nb_drone_per_family=st_nb_drone_per_family,
    angle_takeoff=st_angle_takeoff,
)
@slow
def test_get_angle_takeoff_from_grid(
    nb_x: int,
    nb_y: int,
    nb_drone_per_family: int,
    angle_takeoff: float,
) -> None:
    grid_configuration = GridConfiguration(
        nb_x=nb_x,
        nb_y=nb_y,
        nb_drone_per_family=nb_drone_per_family,
        step=1.5,
        angle_takeoff=angle_takeoff,
    )
    grid = get_grid_from_configuration(grid_configuration)
    assert (
        angle_distance(
            get_angle_takeoff_from_grid(grid, grid_configuration.nb_drone_per_family),
            grid_configuration.angle_takeoff,
        )
        < 1e-6
    )
