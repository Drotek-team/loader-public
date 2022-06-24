from src.drones_manager.drone.drone_encoder import DroneEncoder

from .....drones_manager.drone.drone import Drone
from .....parameter.parameter import IostarParameter
from .dances_size_check_report import DanceSizeCheckReport


def apply_dance_size_check_procedure(
    drone: Drone,
    drone_encoder: DroneEncoder,
    dance_size_check_report: DanceSizeCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    dance_size_check_report.validation = (
        drone_encoder.dance_size(drone) < iostar_parameter.dance_size_max
    )
