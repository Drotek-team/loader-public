from ..iostar_json.iostar_json_gcs import IostarJsonGcs
from ..migration_dp_binary.drone_decoding_procedure import decode_drone
from ..show_px4.show_px4 import ShowPx4


def ijg_to_sp_procedure(iostar_json_gcs: IostarJsonGcs) -> ShowPx4:
    return ShowPx4(
        [
            decode_drone(
                family_index * iostar_json_gcs.nb_drones_per_family + drone_index,
                binary_dance.dance,
            )
            for family_index, family in enumerate(iostar_json_gcs.show.families)
            for drone_index, binary_dance in enumerate(family.drones)
        ]
    )
