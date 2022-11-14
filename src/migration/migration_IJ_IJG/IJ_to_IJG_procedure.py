from typing import Dict, List

from ...iostar_json.iostar_json import IostarJson
from ...iostar_json_gcs.iostar_json_gcs import IostarJsonGCS
from ...parameter.parameter import JsonBinaryParameter, Parameter
from ...show_px4.drone_px4.drone_px4 import DronePx4
from ..migration_IJ_SP.IJ_to_SP_procedure import IJ_to_SP_procedure
from ..migration_IJ_SP.IJ_to_SP_report import IJ_to_SP_report
from ..migration_IJ_SP.migration_DP_binary.drone_encoding_procedure import encode_drone
from .migration_SC.DP_to_SC_procedure import DP_to_SC_procedure


def get_family_dict_from_show_px4(
    show_px4_family: List[DronePx4],
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
            for drone_px4_family in show_px4_family
        ],
    }


# TO DO: test this thing REALLY well
def IJ_to_IJG_procedure(iostar_json: IostarJson, parameter: Parameter) -> IostarJsonGCS:
    show_px4 = IJ_to_SP_procedure(
        iostar_json,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        IJ_to_SP_report(),
    )
    show_configuration = DP_to_SC_procedure(show_px4)
    return IostarJsonGCS(
        **{
            "show": {
                "families": [
                    get_family_dict_from_show_px4(
                        show_px4.drones[
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
