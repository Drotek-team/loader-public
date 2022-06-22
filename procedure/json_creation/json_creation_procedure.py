from ...drones_manager.drones_manager import DronesManager
from ...family_manager.family_manager import FamilyManager
from ...json_convertor.json_convertor import Show
from .json_creation_report import JsonCreationReport


def apply_json_creation_procedure(
    drones_manager: DronesManager,
    family_manager: FamilyManager,
    json_creation_report: JsonCreationReport,
) -> None:
    show = Show()
    show.update_families(drones_manager, family_manager)
    show.update_parameter(
        family_manager.nb_x,
        family_manager.nb_y,
        family_manager.step,
        family_manager.angle_takeoff_degree(drones_manager.first_horizontal_positions),
        drones_manager.convex_hull,
    )
