from typing import Dict, List, Tuple

from ...drones_manager.drones_manager import Drone, DronesManager
from ...family_manager.family_manager import FamilyManager
from .json_convertion_tools.drone_encoder import DroneEncoder
from .json_extraction_report import JsonExtractionReport


def get_nb_drone_per_family(json_dict: Dict) -> int:
    return len(json_dict["dances"][0])


def get_drone(json_dict: Dict) -> List[Drone]:
    drone_encoder = DroneEncoder()
    return [drone_encoder.decode_drone(json_drone) for json_drone in json_dict]


def apply_json_extraction_procedure(
    json_dict: Dict, json_extraction_report: JsonExtractionReport
) -> Tuple[DronesManager, FamilyManager]:
    drones_manager = DronesManager(get_drone(json_dict))
    family_manager = FamilyManager(
        json_dict["nb_x"],
        json_dict["nb_y"],
        get_nb_drone_per_family(json_dict),
        json_dict["step"],
        json_dict["angle_takeoff"],
    )
    json_extraction_report.validation = True
    return drones_manager, family_manager
