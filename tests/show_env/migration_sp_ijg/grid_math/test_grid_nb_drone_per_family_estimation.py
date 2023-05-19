from hypothesis import given
from loader.shows.migrations.grid_math.grid import (
    GridConfiguration,
    get_grid_from_configuration,
)
from loader.shows.migrations.grid_math.grid_nb_per_family_estimation import (
    get_nb_drone_per_family_from_grid,
)

from tests.strategies import (
    st_nb_drone_per_family,
    st_nb_x,
    st_nb_y,
)


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
    assert (
        get_nb_drone_per_family_from_grid(
            get_grid_from_configuration(
                GridConfiguration(
                    nb_x=nb_x,
                    nb_y=nb_y,
                    nb_drone_per_family=nb_drone_per_family,
                ),
            ),
        )
        == nb_drone_per_family
    )
