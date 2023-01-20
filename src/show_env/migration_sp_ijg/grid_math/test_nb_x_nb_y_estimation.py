from hypothesis import given
from hypothesis import strategies as st

from .grid import GridConfiguration, get_grid_from_configuration
from .grid_angle_estimation import get_angle_takeoff_from_grid
from .grid_nb_x_nb_y_estimation import get_nb_x_nb_y_from_grid


@given(
    nb_x=st.integers(2, 4),
    nb_y=st.integers(1, 2),
    nb_drone_per_family=st.integers(1, 3),
    angle_takeoff=st.integers(0, 360),
)
def test_get_nb_drone_per_family_from_grid_standard_grids(
    nb_x: int, nb_y: int, nb_drone_per_family: int, angle_takeoff: int
):
    grid_configuration = GridConfiguration(
        nb_x=nb_x,
        nb_y=nb_y,
        nb_drone_per_family=nb_drone_per_family,
        angle_takeoff=angle_takeoff,
    )
    grid = get_grid_from_configuration(grid_configuration)
    if not (
        get_nb_x_nb_y_from_grid(
            grid,
            grid_configuration.nb_drone_per_family,
            get_angle_takeoff_from_grid(grid, nb_drone_per_family),
        )
        == (
            grid_configuration.nb_x,
            grid_configuration.nb_y,
        )
    ):
        raise ValueError(
            grid,
            grid_configuration,
            get_nb_x_nb_y_from_grid(
                grid,
                grid_configuration.nb_drone_per_family,
                get_angle_takeoff_from_grid(grid, nb_drone_per_family),
            ),
        )
