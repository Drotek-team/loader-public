from ..iostar_json.show_configuration import ShowConfiguration
from ..iostar_json.show_configuration_gcs import ShowConfigurationGcs
from ..show_user.show_user import ShowUser
from .grid_math.grid import get_grid_from_show_user
from .grid_math.grid_angle_estimation import get_angle_takeoff_from_grid
from .grid_math.grid_nb_per_family_estimation import get_nb_drone_per_family_from_grid
from .grid_math.grid_nb_x_nb_y_estimation import get_nb_x_nb_y_from_grid
from .grid_math.grid_step_estimation import get_step_from_grid


# TODO: make this properly
def sc_to_scg(show_configuration: ShowConfiguration) -> ShowConfigurationGcs:
    return ShowConfigurationGcs(
        nb_x=show_configuration.nb_x,
        nb_y=show_configuration.nb_y,
        nb_drone_per_family=show_configuration.nb_drone_per_family,
        step=int(show_configuration.step),
        angle_takeoff=int(show_configuration.angle_takeoff),
        duration=int(show_configuration.duration),
        hull=[(int(point[0]), int(point[1])) for point in show_configuration.hull],
        altitude_range=(
            int(show_configuration.altitude_range[0]),
            int(show_configuration.altitude_range[1]),
        ),
    )


# TODO: test this with hypothesis
def sp_to_sc_procedure(show_user: ShowUser) -> ShowConfigurationGcs:
    grid = get_grid_from_show_user(show_user)
    nb_drone_per_family = get_nb_drone_per_family_from_grid(grid)
    step = get_step_from_grid(grid)
    angle_takeoff = get_angle_takeoff_from_grid(grid, nb_drone_per_family)
    nb_x, nb_y = get_nb_x_nb_y_from_grid(grid, nb_drone_per_family, angle_takeoff)
    return sc_to_scg(
        ShowConfiguration(
            nb_x=nb_x,
            nb_y=nb_y,
            nb_drone_per_family=nb_drone_per_family,
            step=step,
            angle_takeoff=angle_takeoff,
            duration=show_user.duration,
            hull=show_user.convex_hull,
            altitude_range=show_user.altitude_range,
        )
    )
