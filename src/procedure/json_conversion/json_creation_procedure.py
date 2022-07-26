from ...drones_manager.drones_manager import DronesManager
from ...family_manager.family_manager import FamilyManager
from ...parameter.parameter import JsonFormatParameter
from .json_convertion_tools.drone_encoding_procedure import encode_drone
from .json_convertion_tools.show_creation import Show
from .json_creation_report import JsonCreationReport


def apply_json_creation_procedure(
    drones_manager: DronesManager,
    family_manager: FamilyManager,
    json_format_parameter: JsonFormatParameter,
    json_creation_report: JsonCreationReport,
) -> None:
    show = Show(
        nb_x=family_manager.nb_x,
        nb_y=family_manager.nb_y,
        step=family_manager.step_takeoff,
        angle_takeoff=family_manager.angle_takeoff,
        duration=drones_manager.duration,
        hull=drones_manager.convex_hull,
        altitude_range=drones_manager.altitude_range,
    )
    show.update_families(
        [drone_export.first_xyz for drone_export in drones_manager.drones],
        [
            encode_drone(drone_export, json_format_parameter, drone_encoding_report)
            for drone_export, drone_encoding_report in zip(
                drones_manager.drones, json_creation_report.drones_encoding_report
            )
        ],
        family_manager,
    )
    json_creation_report.update()
