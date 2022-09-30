from ...show_user.show_user import FamilyUser

from ...parameter.parameter import JsonBinaryParameter, IostarParameter
from .IJ_to_DP_report import IJ_to_DP_report
from ...drones_px4.drones_px4 import DronesPx4
from .migration_DP_B.drone_decoding_procedure import decode_drone
from ...iostar_json.iostar_json import IostarJson, Show


def get_nb_drone_per_family(json_show: Show) -> int:
    return len(json_show.families[0].drones)


def IJ_to_DP_procedure(
    iostar_json: IostarJson,
    iostar_parameter: IostarParameter,
    json_binary_parameter: JsonBinaryParameter,
    json_extraction_report: IJ_to_DP_report,
) -> DronesPx4:
    nb_drone_per_family = get_nb_drone_per_family(iostar_json.show)
    drones_px4 = DronesPx4(
        [
            decode_drone(
                drone_json.dance,
                family_index * nb_drone_per_family + drone_index,
                iostar_parameter,
                json_binary_parameter,
                json_extraction_report.drones_decoding_report[drone_index],
            )
            for family_index, family in enumerate(iostar_json.show.families)
            for drone_index, drone_json in enumerate(family.drones)
        ]
    )
    return drones_px4


def IJ_to_FU_procedure(iostar_json: IostarJson) -> FamilyUser:
    family_user = FamilyUser(
        nb_x=iostar_json.show.nb_x,
        nb_y=iostar_json.show.nb_y,
        nb_drone_per_family=get_nb_drone_per_family(iostar_json.show),
        step_takeoff=iostar_json.show.step,
        angle_takeoff=iostar_json.show.angle_takeoff,
    )
    return family_user
