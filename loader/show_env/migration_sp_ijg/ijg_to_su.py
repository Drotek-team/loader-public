from typing import List

from loader.show_env.autopilot_format.drone_px4 import DronePx4
from loader.show_env.iostar_json.iostar_json_gcs import IostarJsonGcs
from loader.show_env.migration_dp_binary.drone_decoding import decode_drone
from loader.show_env.migration_sp_su.sp_to_su import sp_to_su
from loader.show_env.show_user import ShowUser


def ijg_to_sp(iostar_json_gcs: IostarJsonGcs) -> List[DronePx4]:
    return [
        decode_drone(
            family_index * iostar_json_gcs.nb_drones_per_family + drone_index,
            binary_dance.dance,
        )
        for family_index, family in enumerate(iostar_json_gcs.show.families)
        for drone_index, binary_dance in enumerate(family.drones)
    ]


def ijg_to_su(iostar_json_gcs: IostarJsonGcs) -> ShowUser:
    return sp_to_su(ijg_to_sp(iostar_json_gcs))
