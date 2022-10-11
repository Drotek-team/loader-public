from ....show_simulation.drone_simulation import DronesSimulation
from ....iostar_json.show_configuration import ShowConfiguration
from .grid_math.grid import Grid
from .grid_math.grid_angle_estimation import get_angle_takeoff_from_grid
from .grid_math.grid_nb_per_family_estimation import (
    get_nb_drone_per_family_from_grid,
)
from .grid_math.grid_step_estimation import get_step_from_grid
from .grid_math.grid_nb_x_nb_y_estimation import get_nb_x_nb_y_from_grid

# ### TO DO: deal with the nb_drone = 0, nb_drone = 1 later
def DP_to_SC_procedure(drones_simulation: DronesSimulation) -> ShowConfiguration:
    grid = Grid(drones_simulation.first_horizontal_positions)
    angle_takeoff = get_angle_takeoff_from_grid(grid)
    nb_drone_per_family = get_nb_drone_per_family_from_grid(grid)
    step = get_step_from_grid(grid)
    nb_x, nb_y = get_nb_x_nb_y_from_grid(grid)
    return ShowConfiguration(
        nb_x,
        nb_y,
        nb_drone_per_family,
        step,
        angle_takeoff,
        drones_simulation.duration,
        drones_simulation.convex_hull,
        drones_simulation.altitude_range,
    )
