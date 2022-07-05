from typing import Dict, Tuple

from ...drones_manager.drones_manager import DronesManager
from ...family_manager.family_manager import FamilyManager
from ...parameter.parameter import JsonConvertionParameter
from .json_convertion_tools.drone_decoding_procedure import decode_drone
from .json_extraction_report import JsonExtractionReport


def get_nb_drone_per_family(json_dict: Dict) -> int:
    return len(json_dict["dances"][0])


def apply_json_extraction_procedure(
    json_dict: Dict,
    json_convertion_parameter: JsonConvertionParameter,
    json_extraction_report: JsonExtractionReport,
) -> Tuple[DronesManager, FamilyManager]:
    drones_manager = DronesManager(
        [
            decode_drone(
                json_drone,
                json_convertion_parameter,
                json_extraction_report.drones_decoding_report[drone_index],
            )
            for drone_index, json_drone in enumerate(json_dict)
        ]
    )
    family_manager = FamilyManager(
        json_dict["nb_x"],
        json_dict["nb_y"],
        get_nb_drone_per_family(json_dict),
        json_dict["step"],
        json_dict["angle_takeoff"],
    )
    json_extraction_report.validation = True
    return drones_manager, family_manager
