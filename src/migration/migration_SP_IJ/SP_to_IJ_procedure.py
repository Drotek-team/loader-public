from ...iostar_json.iostar_json import IostarJson
from ...show_px4.show_px4 import ShowPx4
from ..migration_DP_binary.drone_encoding_procedure import encode_drone


def SP_to_IJG_procedure(show_px4: ShowPx4) -> IostarJson:
    return IostarJson(
        **{
            "binary_dances": [encode_drone(drone_px4) for drone_px4 in show_px4],
        }
    )
