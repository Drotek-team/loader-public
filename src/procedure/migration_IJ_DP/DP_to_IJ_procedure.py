from ...parameter.parameter import JsonBinaryParameter, IostarParameter
from ...iostar_json.iostar_json import IostarJson
from ...show_user.show_user import FamilyUser
from ...drones_px4.drones_px4 import DronesPx4, DronePx4
from typing import List, Dict
from .migration_DP_B.drone_encoding_procedure import encode_drone


def get_family_dict_from_drones_px4(
    drones_px4_family: List[DronePx4],
) -> Dict:
    return {
        "drones": [
            encode_drone(drone_px4_family) for drone_px4_family in drones_px4_family
        ],
        "x": drones_px4_family[0].first_xyz[0],
        "y": drones_px4_family[0].first_xyz[1],
        "z": drones_px4_family[0].first_xyz[2],
    }


def DP_to_IJ_procedure(
    drones_px4: DronesPx4,
    family_user: FamilyUser,
    iostar_parameter: IostarParameter,
    json_binary_parameter: JsonBinaryParameter,
) -> None:
    show = IostarJson(
        **{
            "families": [
                get_family_dict_from_drones_px4(
                    drones_px4.drones[
                        family_user.nb_drone_per_family
                        * family_index : family_user.nb_drone_per_family
                        * family_index
                        + family_user.nb_drone_per_family
                    ]
                )
                for family_index in range(family_user.nb_x * family_user.nb_y)
            ],
            "nb_x": family_user.nb_x,
            "nb_y": family_user.nb_y,
            "step": family_user.step_takeoff,
            "angle_takeoff": family_user.angle_takeoff,
            "duration": drones_px4.duration,
            "hull": drones_px4.convex_hull,
            "altitude_range": drones_px4.altitude_range,
        }
    )

    # json = show.get_json()
    # filename = "popo.json"

    # with open(filename, "w") as f:
    #     f.write(json)
