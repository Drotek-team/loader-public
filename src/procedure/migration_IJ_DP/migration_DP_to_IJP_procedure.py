from ...drones_px4.drones_px4 import DronesPx4

from typing import Tuple
from ...iostar_json.show_configuration import ShowConfiguration


def get_nb_drone_per_family_from_drones_px4(
    drones_px4: DronesPx4, angle_takeoff: float
) -> int:
    pass


def get_nb_x_nb_y_from_drones_px4(
    drones_px4: DronesPx4, angle_takeoff: float
) -> Tuple[int, int]:
    pass


def get_step_from_drones_px4(drones_px4: DronesPx4) -> float:
    pass


def get_angle_takeoff_from_drones_px4(drones_px4: DronesPx4) -> int:
    pass


def DP_to_IJP_procedure(drones_px4: DronesPx4) -> ShowConfiguration:
    pass
