from typing import Dict, Tuple

from import_report import ImportReport

from ..drones_manager.drones_manager import DronesManager
from ..family_manager.family_manager import FamilyManager
from .json_conversion.json_extraction_procedure import apply_json_extraction_procedure
from .show_check.show_check_procedure import apply_show_check_procedure


def apply_import_procedure(
    json_dict: Dict,
    import_report: ImportReport,
) -> Tuple[DronesManager, FamilyManager]:
    drones_manager, family_manager = apply_json_extraction_procedure(
        json_dict, import_report.json_extraction_report
    )
    apply_show_check_procedure(
        drones_manager, family_manager, import_report.show_check_report
    )
    return drones_manager, family_manager
