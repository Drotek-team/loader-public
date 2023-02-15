from typing import List

from loader.show_env.autopilot_format.drone_px4 import DronePx4
from loader.show_env.iostar_json import IostarJson
from loader.show_env.migration_dp_binary.drone_encoding import encode_drone
from loader.show_env.migration_sp_su.su_to_sp import su_to_sp
from loader.show_env.show_user import ShowUser


def sp_to_ij(autopilot_format: List[DronePx4]) -> IostarJson:
    return IostarJson(
        binary_dances=[encode_drone(drone_px4) for drone_px4 in autopilot_format],
    )


def su_to_ij(show_user: ShowUser) -> IostarJson:
    return sp_to_ij(su_to_sp(show_user))
