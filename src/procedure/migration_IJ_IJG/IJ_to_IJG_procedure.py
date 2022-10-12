from ...iostar_json.iostar_json import IostarJson
from ...iostar_json_gcs.iostar_json_gcs import IostarJsonGCS
from .migration_SC.DP_to_SC_procedure import DP_to_SC_procedure
from ..migration_IJ_DP.IJ_to_DP_procedure import IJ_to_DP_procedure
from ...parameter.parameter import Parameter
from typing import List, Dict
from ...drones_px4.drone_px4.drone_px4 import DronePx4
from ...parameter.parameter import JsonBinaryParameter
from ..migration_IJ_DP.migration_DP_binary.drone_encoding_procedure import encode_drone


def get_family_dict_from_drones_px4(
    drones_px4_family: List[DronePx4],
    json_binary_parameter: JsonBinaryParameter,
) -> Dict:
    return {
        "dances": [
            {
                "dance": encode_drone(
                    drone_px4_family,
                    json_binary_parameter,
                )
            }
            for drone_px4_family in drones_px4_family
        ],
    }


def IJ_to_IJG_procedure(iostar_json: IostarJson, parameter: Parameter) -> IostarJsonGCS:
    drones_px4 = IJ_to_DP_procedure(
        iostar_json,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
    )
    show_configuration = DP_to_SC_procedure(drones_px4)
    return IostarJsonGCS(
        **{
            "show": {
                "families": [
                    get_family_dict_from_drones_px4(
                        drones_px4[
                            show_configuration.nb_drone_per_family
                            * family_index : show_configuration.nb_drone_per_family
                            * family_index
                            + show_configuration.nb_drone_per_family
                        ],
                        parameter.json_binary_parameter,
                    )
                    for family_index in range(
                        show_configuration.nb_x * show_configuration.nb_y
                    )
                ],
            },
            "duration": show_configuration.duration,
            "hull": show_configuration.hull,
            "altitude_range": show_configuration.altitude_range,
            "step": show_configuration.step,
            "nb_x": show_configuration.nb_x,
            "nb_y": show_configuration.nb_y,
            "angle_takeoff": show_configuration.angle_takeoff,
        }
    )
