from typing import Dict, Tuple

from ..drones_manager.drones_manager import DronesManager
from ..family_manager.family_manager import FamilyManager
from ..parameter.parameter import Parameter
from .import_report import ImportReport
from .json_conversion.json_extraction_procedure import apply_json_extraction_procedure
from .show_check.show_check_procedure import apply_show_check_procedure


def apply_import_procedure(
    json_dict: Dict,
    import_report: ImportReport,
) -> Tuple[DronesManager, FamilyManager]:
    parameter = Parameter()
    parameter.load_parameter()
    drones_manager, family_manager = apply_json_extraction_procedure(
        json_dict, parameter.json_format_parameter, import_report.json_extraction_report
    )
    import_report.show_check_report.initialize_drones_check_report(
        len(drones_manager.drones)
    )
    apply_show_check_procedure(
        drones_manager, family_manager, import_report.show_check_report
    )
    import_report.update()
    return drones_manager, family_manager
