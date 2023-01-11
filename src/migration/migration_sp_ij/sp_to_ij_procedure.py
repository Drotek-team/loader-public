from iostar_json.iostar_json import IostarJson
from migration.migration_dp_binary.drone_encoding_procedure import encode_drone
from show_px4.show_px4 import ShowPx4


def sp_to_ij_procedure(show_px4: ShowPx4) -> IostarJson:
    return IostarJson(
        **{
            "binary_dances": [encode_drone(drone_px4) for drone_px4 in show_px4],
        }
    )
