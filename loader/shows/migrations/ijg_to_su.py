from typing import List

from loader.shows.drone_px4 import DronePx4
from loader.shows.iostar_json_gcs.iostar_json_gcs import IostarJsonGcs
from loader.shows.show_user import ShowUser


def ijg_to_sp(iostar_json_gcs: IostarJsonGcs) -> List[DronePx4]:
    return [
        DronePx4.from_binary(
            family_index * iostar_json_gcs.nb_drones_per_family + drone_index,
            binary_dance.dance,
        )
        for family_index, family in enumerate(iostar_json_gcs.show.families)
        for drone_index, binary_dance in enumerate(family.drones)
    ]


def ijg_to_su(iostar_json_gcs: IostarJsonGcs) -> ShowUser:
    return ShowUser.from_autopilot_format(ijg_to_sp(iostar_json_gcs))
