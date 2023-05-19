import numpy as np
from hypothesis import given
from loader.shows.grid_configuration.grid import Grid, GridConfiguration

from tests.strategies import (
    slow,
    st_angle_takeoff,
    st_nb_drone_per_family,
    st_nb_x,
    st_nb_y,
    st_step_takeoff,
)


@given(
    nb_x=st_nb_x,
    nb_y=st_nb_y,
    nb_drone_per_family=st_nb_drone_per_family,
    step_takeoff=st_step_takeoff,
    angle_takeoff=st_angle_takeoff,
)
@slow
def test_get_step_from_grid_hypothesis(
    nb_x: int,
    nb_y: int,
    nb_drone_per_family: int,
    step_takeoff: int,
    angle_takeoff: int,
) -> None:
    grid = Grid.from_grid_configuration(
        GridConfiguration(
            nb_x=nb_x,
            nb_y=nb_y,
            nb_drone_per_family=nb_drone_per_family,
            step=step_takeoff,
            angle_takeoff=angle_takeoff,
        ),
    )
    if grid.is_grid_one_family():
        return
    np.testing.assert_allclose(grid.get_step(), step_takeoff)
