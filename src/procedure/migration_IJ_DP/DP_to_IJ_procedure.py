from ...parameter.parameter import JsonBinaryParameter
from ...iostar_json.iostar_json import IostarJson
from ...drones_px4.drones_px4 import DronesPx4, DronePx4
from typing import List, Dict
from .migration_DP_binary.drone_encoding_procedure import encode_drone


def DP_to_IJ_procedure(
    drones_px4: DronesPx4, json_binary_parameter: JsonBinaryParameter
) -> None:
    show = IostarJson(
        **{
            "show": {
                "binary_dances": [
                    encode_drone(
                        drone_px4,
                        json_binary_parameter,
                    )
                    for drone_px4 in drones_px4
                ],
            }
        }
    )

    # json = show.get_json()
    # filename = "popo.json"

    # with open(filename, "w") as f:
    #     f.write(json)
