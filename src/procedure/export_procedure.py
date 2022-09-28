from .show_check.show_check_report import ShowCheckReport
from ..drones_user.drones_user import DronesUser
from ..family_manager.family_manager import FamilyManager
from ..parameter.parameter import Parameter
from .export_report import ExportReport
from .json_conversion.json_creation_procedure import apply_json_creation_procedure
from .show_check.show_check_procedure import apply_show_check_procedure
from .json_conversion.json_creation_report import JsonCreationReport


def apply_export_procedure(
    drones_user: DronesUser,
    family_manager: FamilyManager,
    export_report: ExportReport,
    parameter: Parameter,
) -> None:
    export_report.show_check_report = ShowCheckReport(len(drones_user.drones))
    apply_show_check_procedure(
        drones_user,
        family_manager,
        export_report.show_check_report,
        parameter,
    )
    export_report.json_creation_report = JsonCreationReport(len(drones_user.drones))
    apply_json_creation_procedure(
        drones_user,
        family_manager,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        export_report.json_creation_report,
    )
    export_report.update()
