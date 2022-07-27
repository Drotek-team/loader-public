from ..drones_manager.drones_manager import DronesManager
from ..family_manager.family_manager import FamilyManager
from ..parameter.parameter import Parameter
from .export_report import ExportReport
from .json_conversion.json_creation_procedure import apply_json_creation_procedure
from .show_check.show_check_procedure import apply_show_check_procedure


def apply_export_procedure(
    drones_manager: DronesManager,
    family_manager: FamilyManager,
    export_report: ExportReport,
    parameter: Parameter,
) -> None:
    export_report.show_check_report.initialize_drones_check_report(
        len(drones_manager.drones)
    )
    apply_show_check_procedure(
        drones_manager,
        family_manager,
        export_report.show_check_report,
        parameter,
    )
    export_report.json_creation_report.initialize_drones_encoding_report(
        len(drones_manager.drones)
    )
    apply_json_creation_procedure(
        drones_manager,
        family_manager,
        parameter.json_format_parameter,
        export_report.json_creation_report,
    )
    export_report.update()
