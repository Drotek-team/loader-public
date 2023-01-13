from typing import Dict, List

from ...show_px4.drone_px4.drone_px4 import DronePx4
from ...show_px4.show_px4 import ShowPx4
from ..iostar_json.iostar_json_gcs import IostarJsonGCS
from ..migration_dp_binary.drone_encoding_procedure import encode_drone
from .sp_to_sc_procedure import sp_to_sc_procedure


def get_family_dict_from_show_px4(
    show_px4_family: List[DronePx4],
) -> Dict:
    return {
        "drones": [
            {
                "dance": encode_drone(
                    drone_px4_family,
                )
            }
            for drone_px4_family in show_px4_family
        ],
        "x": show_px4_family[0].first_xyz[0],
        "y": show_px4_family[0].first_xyz[1],
        "z": show_px4_family[0].first_xyz[2],
    }


def sp_to_ijg_procedure(show_px4: ShowPx4) -> IostarJsonGCS:
    show_configuration = sp_to_sc_procedure(show_px4)
    return IostarJsonGCS(
        **{
            "show": {
                "families": [
                    get_family_dict_from_show_px4(
                        show_px4[
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
                "duration": show_configuration.duration,
                "hull": show_configuration.hull,
                "altitude_range": show_configuration.altitude_range,
                "step": show_configuration.step,
                "nb_x": show_configuration.nb_x,
                "nb_y": show_configuration.nb_y,
                "angle_takeoff": show_configuration.angle_takeoff,
            }
        }
    )
