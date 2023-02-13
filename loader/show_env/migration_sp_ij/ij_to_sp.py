from loader.show_env.iostar_json.iostar_json import IostarJson
from loader.show_env.migration_dp_binary.drone_decoding import decode_drone
from loader.show_env.show_px4.show_px4 import ShowPx4


def ij_to_sp(iostar_json: IostarJson) -> ShowPx4:
    return ShowPx4(
        [
            decode_drone(drone_index, binary_dance)
            for drone_index, binary_dance in enumerate(iostar_json.binary_dances)
        ],
    )