from hypothesis import given
from loader.schemas.grid_configuration import GridConfiguration
from loader.schemas.grid_configuration.grid import Grid
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import get_valid_show_user

from tests.strategies import slow, st_angle_takeoff, st_nb_drone_per_family, st_nb_x, st_nb_y


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
        matrix=get_matrix(nb_x=nb_x, nb_y=nb_y, nb_drone_per_family=nb_drone_per_family),
        angle_takeoff=angle_takeoff,
    )
    grid = Grid.from_show_user(get_valid_show_user(grid_configuration))
    assert grid.get_nb_x_nb_y(
        grid_configuration.nb_drone_per_family,
        grid_configuration.angle_takeoff,
    ) == (
        grid_configuration.nb_x,
        grid_configuration.nb_y,
    )
