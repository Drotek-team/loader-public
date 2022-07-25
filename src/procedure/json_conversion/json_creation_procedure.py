from ...drones_manager.drones_manager import DronesManager
from ...family_manager.family_manager import FamilyManager
from .json_convertion_tools.show_creation import Show
from .json_creation_report import JsonCreationReport


def apply_json_creation_procedure(
    drones_manager: DronesManager,
    family_manager: FamilyManager,
    json_creation_report: JsonCreationReport,
) -> None:
    show = Show()
    show.update_families(drones_manager, family_manager, json_creation_report)
    show.update_parameter(
        family_manager.nb_x,
        family_manager.nb_y,
        family_manager.step_takeoff,
        family_manager.angle_takeoff,
        drones_manager.convex_hull,
        json_creation_report,
    )
    json_creation_report.update()
