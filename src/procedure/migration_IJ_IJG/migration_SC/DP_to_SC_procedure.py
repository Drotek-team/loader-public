from ....iostar_json.show_configuration import ShowConfiguration
from .grid_math.grid import Grid
from .grid_math.grid_angle_estimation import get_angle_takeoff_from_grid
from .grid_math.grid_nb_per_family_estimation import (
    get_nb_drone_per_family_from_grid,
)
from .grid_math.grid_step_estimation import get_step_from_grid
from .grid_math.grid_nb_x_nb_y_estimation import get_nb_x_nb_y_from_grid
from ....drones_px4.drones_px4 import DronesPx4


# ### TO DO: deal with the nb_drone = 0, nb_drone = 1 later
def DP_to_SC_procedure(drones_px4: DronesPx4) -> ShowConfiguration:
    grid = Grid(drones_px4.first_horizontal_positions)
    angle_takeoff = get_angle_takeoff_from_grid(grid)
    nb_drone_per_family = get_nb_drone_per_family_from_grid(grid)
    step = get_step_from_grid(grid)
    nb_x, nb_y = get_nb_x_nb_y_from_grid(grid)
    return ShowConfiguration(
        nb_x=nb_x,
        nb_y=nb_y,
        nb_drone_per_family=nb_drone_per_family,
        step=step,
        angle_takeoff=angle_takeoff,
        duration=drones_px4.duration,
        convex_hull=drones_px4.convex_hull,
        altitude_range=drones_px4.altitude_range,
    )
