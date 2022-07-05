from ..drones_manager.drones_manager import DronesManager
from ..family_manager.family_manager import FamilyManager
from .export_report import ExportReport
from .json_conversion.json_creation_procedure import apply_json_creation_procedure
from .show_check.show_check_procedure import apply_show_check_procedure


def apply_export_procedure(
    drones_manager: DronesManager,
    family_manager: FamilyManager,
    export_report: ExportReport,
) -> None:
    drones_manager.apply_dances_size_relief()
    apply_show_check_procedure(
        drones_manager,
        family_manager,
        export_report.show_check_report,
    )
    apply_json_creation_procedure(
        drones_manager, family_manager, export_report.json_creation_report
    )
