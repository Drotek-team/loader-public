from ...parameter.parameter import JsonBinaryParameter
from ...iostar_json.iostar_json import IostarJson
from ...drones_px4.drones_px4 import DronesPx4, DronePx4
from typing import List, Dict
from .migration_DP_B.drone_encoding_procedure import encode_drone


def get_family_dict_from_drones_px4(
    drones_px4_family: List[DronePx4],
    json_binary_parameter: JsonBinaryParameter,
) -> Dict:
    return {
        "drones": [
            {
                "dance": encode_drone(
                    drone_px4_family,
                    json_binary_parameter,
                )
            }
            for drone_px4_family in drones_px4_family
        ],
        "x": drones_px4_family[0].first_xyz[0],
        "y": drones_px4_family[0].first_xyz[1],
        "z": drones_px4_family[0].first_xyz[2],
    }


def DP_to_IJ_procedure(
    drones_px4: DronesPx4,
    json_binary_parameter: JsonBinaryParameter,
) -> None:
    pass
    # show = IostarJson(
    #     **{
    #         "show": {
    #             "families": [
    #                 get_family_dict_from_drones_px4(
    #                     drones_px4.drones[
    #                         iostar_json.show.nb_drone_per_family
    #                         * family_index : iostar_json_parameter.nb_drone_per_family
    #                         * family_index
    #                         + iostar_json_parameter.nb_drone_per_family
    #                     ],
    #                     json_binary_parameter,
    #                 )
    #                 for family_index in range(
    #                     iostar_json_parameter.nb_x * iostar_json_parameter.nb_y
    #                 )
    #             ],
    #             "nb_x": iostar_json_parameter.nb_x,
    #             "nb_y": iostar_json_parameter.nb_y,
    #             "step": iostar_json_parameter.step_takeoff,
    #             "angle_takeoff": iostar_json_parameter.angle_takeoff,
    #             "duration": drones_px4.duration,
    #             "hull": drones_px4.convex_hull,
    #             "altitude_range": drones_px4.altitude_range,
    #         }
    #     }
    # )

    # json = show.get_json()
    # filename = "popo.json"

    # with open(filename, "w") as f:
    #     f.write(json)
