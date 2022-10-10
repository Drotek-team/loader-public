from ....show_simulation.drone_simulation import DronesSimulation
from ....iostar_json.show_configuration import ShowConfiguration
from .grid_math import HorizontalPosition
from .grid_math import (
    get_angle_takeoff_from_drones_px4,
    get_nb_x_nb_y_from_drones_px4,
    get_step_from_drones_px4,
    get_nb_drone_per_family_from_drones_px4,
)

# ### TO DO: deal with the nb_drone = 0, nb_drone = 1 later
def DP_to_SC_procedure(drones_simulation: DronesSimulation) -> ShowConfiguration:
    horizontal_positions = [
        HorizontalPosition(
            drone_index, first_horizontal_position[0], first_horizontal_position[1]
        )
        for drone_index, first_horizontal_position in enumerate(
            drones_simulation.first_horizontal_positions
        )
    ]
    angle_takeoff = get_angle_takeoff_from_drones_px4(horizontal_positions.copy())
    nb_x, nb_y = 0, 0
    return ShowConfiguration()
