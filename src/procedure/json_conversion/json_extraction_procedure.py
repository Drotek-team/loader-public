from typing import Dict, Tuple

from ...drones_px4.drones_user import DronesPx4
from ...family_user.family_user import FamilyUser
from ...parameter.parameter import JsonBinaryParameter, IostarParameter
from .json_convertion_tools.drone_decoding_procedure import decode_drone
from .json_extraction_report import JsonExtractionReport


def get_nb_drone_per_family(json_show: Dict) -> int:
    return len(json_show["families"][0]["drones"])


def apply_json_extraction_procedure(
    json_dict: Dict,
    iostar_parameter: IostarParameter,
    json_binary_parameter: JsonBinaryParameter,
    json_extraction_report: JsonExtractionReport,
) -> Tuple[DronesPx4, FamilyUser]:
    json_show = json_dict["show"]
    nb_drone_per_family = get_nb_drone_per_family(json_show)
    drones_user = DronesPx4(
        [
            decode_drone(
                drone_json["dance"],
                family_index * nb_drone_per_family + drone_index,
                iostar_parameter,
                json_binary_parameter,
                json_extraction_report.drones_decoding_report[drone_index],
            )
            for family_index, family in enumerate(json_show["families"])
            for drone_index, drone_json in enumerate(family["drones"])
        ]
    )
    family_user = FamilyUser(
        json_show["nb_x"],
        json_show["nb_y"],
        nb_drone_per_family,
        json_show["step"],
        json_show["angle_takeoff"],
        json_show["duration"],
        json_show["altitude_range"],
    )
    json_extraction_report.update()
    return drones_user, family_user
