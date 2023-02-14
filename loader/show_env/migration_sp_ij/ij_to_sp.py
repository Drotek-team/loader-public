from typing import List

from loader.show_env.iostar_json import IostarJson
from loader.show_env.migration_dp_binary.drone_decoding import decode_drone
from loader.show_env.show_px4.drone_px4 import DronePx4


def ij_to_sp(iostar_json: IostarJson) -> List[DronePx4]:
    return [
        decode_drone(drone_index, binary_dance)
        for drone_index, binary_dance in enumerate(iostar_json.binary_dances)
    ]
