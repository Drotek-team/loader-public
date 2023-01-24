from ...show_env.migration_dp_binary.drone_encoding_procedure import encode_drone
from ..iostar_json.iostar_json import IostarJson
from ..migration_sp_su.su_to_sp_procedure import su_to_sp_procedure
from ..show_px4.show_px4 import ShowPx4
from ..show_user.show_user import ShowUser


def sp_to_ij_procedure(show_px4: ShowPx4) -> IostarJson:
    return IostarJson(
        **{
            "binary_dances": [encode_drone(drone_px4) for drone_px4 in show_px4],
        }
    )


def su_to_ij_procedure(show_user: ShowUser) -> IostarJson:
    return sp_to_ij_procedure(su_to_sp_procedure(show_user))
