from hypothesis import given
from hypothesis import strategies as st

from .grid import GridConfiguration, get_grid_from_configuration
from .grid_nb_per_family_estimation import get_nb_drone_per_family_from_grid


def test_is_grid_one_family():
    standard_grids = {
        GridConfiguration(
            nb_x=nb_x,
            nb_y=nb_y,
            nb_drone_per_family=nb_drone_per_family,
        ): get_grid_from_configuration(
            GridConfiguration(
                nb_x=nb_x,
                nb_y=nb_y,
                nb_drone_per_family=nb_drone_per_family,
            )
        )
        for nb_x in range(1, 3)
        for nb_y in range(1, 3)
        for nb_drone_per_family in range(1, 5)
    }
    for grid_configuration in standard_grids:
        assert standard_grids[grid_configuration].is_grid_one_family() == (
            grid_configuration.nb_x == 1 and grid_configuration.nb_y == 1
        )


@given(
    nb_x=st.integers(1, 3),
    nb_y=st.integers(1, 3),
    nb_drone_per_family=st.integers(1, 3),
)
def test_get_nb_drone_per_family_from_grid_valid_grid(
    nb_x: int, nb_y: int, nb_drone_per_family: int
):
    assert (
        get_nb_drone_per_family_from_grid(
            get_grid_from_configuration(
                GridConfiguration(
                    nb_x=nb_x, nb_y=nb_y, nb_drone_per_family=nb_drone_per_family
                )
            )
        )
        == nb_drone_per_family
    )
