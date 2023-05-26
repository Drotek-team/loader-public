from hypothesis import given
from loader.schemas.grid_configuration import GridConfiguration
from loader.schemas.grid_configuration.grid import Grid
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import get_valid_show_user

from tests.strategies import st_nb_drone_per_family, st_nb_x, st_nb_y


@given(
    nb_x=st_nb_x,
    nb_y=st_nb_y,
    nb_drone_per_family=st_nb_drone_per_family,
)
def test_get_nb_drone_per_family_from_grid_valid_grid(
    nb_x: int,
    nb_y: int,
    nb_drone_per_family: int,
) -> None:
    show_user = get_valid_show_user(
        GridConfiguration(
            matrix=get_matrix(nb_x=nb_x, nb_y=nb_y, nb_drone_per_family=nb_drone_per_family),
        ),
    )
    assert Grid.from_show_user(show_user).get_nb_drone_per_family() == nb_drone_per_family
