from hypothesis import given
from hypothesis import strategies as st
from loader.show_env.migration_sp_ijg.grid_math.grid import (
    GridConfiguration,
    get_grid_from_configuration,
)
from loader.show_env.migration_sp_ijg.grid_math.grid_nb_per_family_estimation import (
    get_nb_drone_per_family_from_grid,
)


@given(
    nb_x=st.integers(1, 3),
    nb_y=st.integers(1, 3),
    nb_drone_per_family=st.integers(1, 3),
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
