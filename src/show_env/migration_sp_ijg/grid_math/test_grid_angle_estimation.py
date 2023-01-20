import math

import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from .grid import GridConfiguration, get_grid_from_configuration
from .grid_angle_estimation import (
    get_angle_degree_from_vector,
    get_angle_takeoff_from_grid,
)


def test_get_angle_from_vector():
    assert get_angle_degree_from_vector(np.array([1.0, 0])) == math.radians(0)
    assert get_angle_degree_from_vector(np.array([0, 1.0])) == math.radians(90)
    assert get_angle_degree_from_vector(np.array([-1.0, 0])) == math.radians(180)
    assert get_angle_degree_from_vector(np.array([0, -1.0])) == math.radians(-90)
    assert get_angle_degree_from_vector(np.array([1.0, 1.0])) == math.radians(45)
    assert get_angle_degree_from_vector(np.array([-1.0, 1.0])) == math.radians(135)
    assert get_angle_degree_from_vector(np.array([-1.0, -1.0])) == math.radians(-135)
    assert get_angle_degree_from_vector(np.array([1.0, -1.0])) == math.radians(-45)


# https://stackoverflow.com/questions/1878907/how-can-i-find-the-smallest-difference-between-two-angles-around-a-point
def angle_distance(first_angle_radian: float, second_angle_radian: float) -> float:
    first_angle, second_angle = math.degrees(first_angle_radian), math.degrees(
        second_angle_radian
    )
    return abs((second_angle - first_angle + 180) % 360 - 180)


@given(
    nb_x=st.integers(2, 4),
    nb_y=st.integers(1, 4),
    nb_drone_per_family=st.integers(1, 3),
    angle_takeoff=st.floats(0, 0.5 * np.pi),
)
def test_get_angle_takeoff_from_grid(
    nb_x: int,
    nb_y: int,
    nb_drone_per_family: int,
    angle_takeoff: float,
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
    if grid.is_grid_one_family() and angle_takeoff != 0:
        return
    assert (
        angle_distance(
            get_angle_takeoff_from_grid(grid, nb_drone_per_family), angle_takeoff
        )
        < 1e-6
    )
