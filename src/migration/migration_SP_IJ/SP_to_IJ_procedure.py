from typing import Dict, List

from ...iostar_json.iostar_json_gcs import IostarJson
from ...show_px4.drone_px4.drone_px4 import DronePx4
from ...show_px4.show_px4 import ShowPx4
from .migration_DP_binary.drone_encoding_procedure import encode_drone
from .migration_DP_SC.DP_to_SC_procedure import DP_to_SC_procedure


def get_family_dict_from_show_px4(
    show_px4_family: List[DronePx4],
) -> Dict:
    return {
        "dances": [
            {
                "dance": encode_drone(
                    drone_px4_family,
                )
            }
            for drone_px4_family in show_px4_family
        ],
    }


# TO DO: test this thing REALLY well
def SP_to_IJ_procedure(show_px4: ShowPx4) -> IostarJson:
    show_configuration = DP_to_SC_procedure(show_px4)
    return IostarJson(
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
