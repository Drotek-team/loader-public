from ..iostar_json.show_configuration import ShowConfiguration
from ..show_px4.show_px4 import ShowPx4
from .grid_math.grid import Grid, HorizontalPosition
from .grid_math.grid_angle_estimation import get_ned_angle_takeoff_from_grid
from .grid_math.grid_nb_per_family_estimation import get_nb_drone_per_family_from_grid
from .grid_math.grid_nb_x_nb_y_estimation import get_nb_x_nb_y_from_grid
from .grid_math.grid_step_estimation import get_step_from_grid


def sp_to_sc_procedure(show_px4: ShowPx4) -> ShowConfiguration:
    grid = Grid(
        [
            HorizontalPosition(
                drone_index,
                float(horizontal_position[0]),
                float(horizontal_position[1]),
            )
            for drone_index, horizontal_position in enumerate(
                show_px4.first_horizontal_positions
            )
        ]
    )
    angle_takeoff = get_ned_angle_takeoff_from_grid(grid)
    nb_drone_per_family = get_nb_drone_per_family_from_grid(grid)
    step = get_step_from_grid(grid)
    nb_x, nb_y = get_nb_x_nb_y_from_grid(grid, angle_takeoff)
    return ShowConfiguration(
        nb_x=nb_x,
        nb_y=nb_y,
        nb_drone_per_family=nb_drone_per_family,
        step=step,
        angle_takeoff=angle_takeoff,
        duration=show_px4.duration,
        hull=show_px4.convex_hull,
        altitude_range=show_px4.altitude_range,
    )
