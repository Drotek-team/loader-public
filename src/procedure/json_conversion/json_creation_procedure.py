from ...drones_px4.drones_px4 import DronesPx4
from ...family_user.family_user import FamilyUser
from ...parameter.parameter import JsonBinaryParameter, IostarParameter
from .json_convertion_tools.drone_encoding_procedure import encode_drone
from .json_convertion_tools.show_creation import Show
from .json_creation_report import JsonCreationReport


def apply_json_creation_procedure(
    drones_px4: DronesPx4,
    family_user: FamilyUser,
    iostar_parameter: IostarParameter,
    json_binary_parameter: JsonBinaryParameter,
    json_creation_report: JsonCreationReport,
) -> None:
    show = Show(
        nb_x=family_user.nb_x,
        nb_y=family_user.nb_y,
        step=family_user.step_takeoff,
        angle_takeoff=family_user.angle_takeoff,
        duration=drones_px4.duration,
        hull=drones_px4.convex_hull,
        altitude_range=drones_px4.altitude_range,
    )
    show.update_families(
        [drone_user.first_xyz for drone_user in drones_px4.drones],
        [
            encode_drone(
                drone_user,
                iostar_parameter,
                json_binary_parameter,
                drone_encoding_report,
            )
            for drone_user, drone_encoding_report in zip(
                drones_px4.drones, json_creation_report.drones_encoding_report
            )
        ],
        family_user,
    )
    json = show.get_json()
    filename = "popo.json"

    with open(filename, "w") as f:
        f.write(json)

    json_creation_report.update()
