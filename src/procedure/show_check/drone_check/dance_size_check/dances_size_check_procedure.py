from .....drones_manager.drone.drone import Drone
from .....parameter.parameter import IostarParameter
from .dances_size_check_report import DanceSizeCheckReport

from ....json_e

def apply_dance_size_check_procedure(
    drone: Drone,
    drone_encoder: DroneEncoder,
    iostar_parameter: IostarParameter,
    dance_size_check_report: DanceSizeCheckReport,
) -> None:
    dance_size_check_report.validation = (
        drone_encoder.dance_size(drone) < iostar_parameter.dance_size_max
    )
