from ...parameter.parameter import JsonBinaryParameter
from ...iostar_json.iostar_json import IostarJson
from ...show_px4.show_px4 import ShowPx4, DronePx4
from typing import List, Dict
from .migration_DP_binary.drone_encoding_procedure import encode_drone


def DP_to_IJ_procedure(
    show_px4: ShowPx4, json_binary_parameter: JsonBinaryParameter
) -> None:
    show = IostarJson(
        **{
            "show": {
                "binary_dances": [
                    encode_drone(
                        drone_px4,
                        json_binary_parameter,
                    )
                    for drone_px4 in show_px4
                ],
            }
        }
    )

    # json = show.get_json()
    # filename = "popo.json"

    # with open(filename, "w") as f:
    #     f.write(json)
