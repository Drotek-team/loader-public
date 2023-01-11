from ...iostar_json.iostar_json import IostarJson
from ...show_px4.show_px4 import ShowPx4
from ..migration_dp_binary.drone_decoding_procedure import decode_drone


def ij_to_sp_procedure(iostar_json: IostarJson) -> ShowPx4:
    return ShowPx4(
        [
            decode_drone(drone_index, binary_dance)
            for drone_index, binary_dance in enumerate(iostar_json.binary_dances)
        ]
    )
