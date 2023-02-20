import numpy as np
from hypothesis import given
from hypothesis import strategies as st
from loader.show_env.migration_sp_ijg.grid_math.grid import (
    GridConfiguration,
    get_grid_from_configuration,
)
from loader.show_env.migration_sp_ijg.grid_math.grid_step_estimation import (
    get_step_from_grid,
)


@given(
    nb_x=st.integers(1, 3),
    nb_y=st.integers(1, 3),
    nb_drone_per_family=st.integers(1, 2),
    step_takeoff=st.floats(1, 5),
    angle_takeoff=st.floats(0, np.pi),
)
def test_get_nb_drone_per_family_from_grid_valid_grids(
    nb_x: int,
    nb_y: int,
    nb_drone_per_family: int,
    step_takeoff: int,
    angle_takeoff: int,
) -> None:
    grid = get_grid_from_configuration(
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
    np.testing.assert_allclose(
        get_step_from_grid(grid),
        step_takeoff,
    )
