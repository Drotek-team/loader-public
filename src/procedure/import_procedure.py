from typing import Dict, Tuple

from import_report import ImportReport

from ..drones_manager.drones_manager import DronesManager
from ..family_manager.family_manager import FamilyManager
from .drones_creation.drones_creation_procedure import apply_drone_creation_procedure
from .show_check.show_check_procedure import apply_show_check_procedure


def apply_import_procedure(
    json_dict: Dict,
    import_report: ImportReport,
) -> Tuple[DronesManager, FamilyManager]:
    drones_manager, family_manager = apply_drone_creation_procedure(
        json_dict, import_report.drone_creation_report
    )
    apply_show_check_procedure(
        drones_manager, family_manager, import_report.show_check_report
    )
    return drones_manager, family_manager
