from hypothesis import given
from loader.shows.migration_sp_ijg.grid_math.grid import (
    GridConfiguration,
    get_grid_from_configuration,
)
from loader.shows.migration_sp_ijg.grid_math.grid_nb_x_nb_y_estimation import (
    get_nb_x_nb_y_from_grid,
)

from tests.strategies import (
    slow,
    st_angle_takeoff,
    st_nb_drone_per_family,
    st_nb_x,
    st_nb_y,
)


@given(
    nb_x=st_nb_x,
    nb_y=st_nb_y,
    nb_drone_per_family=st_nb_drone_per_family,
    angle_takeoff=st_angle_takeoff,
)
@slow
def test_get_nb_drone_per_family_from_grid_standard_grids(
    nb_x: int,
    nb_y: int,
    nb_drone_per_family: int,
    angle_takeoff: int,
) -> None:
    grid_configuration = GridConfiguration(
        nb_x=nb_x,
        nb_y=nb_y,
        nb_drone_per_family=nb_drone_per_family,
        angle_takeoff=angle_takeoff,
    )
    grid = get_grid_from_configuration(grid_configuration)
    assert get_nb_x_nb_y_from_grid(
        grid,
        grid_configuration.nb_drone_per_family,
        grid_configuration.angle_takeoff,
    ) == (
        grid_configuration.nb_x,
        grid_configuration.nb_y,
    )
