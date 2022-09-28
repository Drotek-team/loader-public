from ...drones_user.drones_user import DronesUser
from ...family_manager.family_manager import FamilyManager
from ...parameter.parameter import JsonBinaryParameter, IostarParameter
from .json_convertion_tools.drone_encoding_procedure import encode_drone
from .json_convertion_tools.show_creation import Show
from .json_creation_report import JsonCreationReport


def apply_json_creation_procedure(
    drones_user: DronesUser,
    family_manager: FamilyManager,
    iostar_parameter: IostarParameter,
    json_binary_parameter: JsonBinaryParameter,
    json_creation_report: JsonCreationReport,
) -> None:
    show = Show(
        nb_x=family_manager.nb_x,
        nb_y=family_manager.nb_y,
        step=family_manager.step_takeoff,
        angle_takeoff=family_manager.angle_takeoff,
        duration=drones_user.duration,
        hull=drones_user.convex_hull,
        altitude_range=drones_user.altitude_range,
    )
    show.update_families(
        [drone_user.first_xyz for drone_user in drones_user.drones],
        [
            encode_drone(
                drone_user,
                iostar_parameter,
                json_binary_parameter,
                drone_encoding_report,
            )
            for drone_user, drone_encoding_report in zip(
                drones_user.drones, json_creation_report.drones_encoding_report
            )
        ],
        family_manager,
    )
    json = show.get_json()
    filename = "popo.json"

    with open(filename, "w") as f:
        f.write(json)

    json_creation_report.update()
