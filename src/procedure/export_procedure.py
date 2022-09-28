from .show_check.show_check_report import ShowCheckReport
from ..drones_px4.drones_user import DronesUser
from ..family_user.family_user import FamilyUser
from ..parameter.parameter import Parameter
from .export_report import ExportReport
from .json_conversion.json_creation_procedure import apply_json_creation_procedure
from .show_check.show_check_procedure import apply_show_check_procedure
from .json_conversion.json_creation_report import JsonCreationReport


def apply_export_procedure(
    drones_user: DronesUser,
    family_user: FamilyUser,
    export_report: ExportReport,
    parameter: Parameter,
) -> None:
    export_report.show_check_report = ShowCheckReport(len(drones_user.drones))
    apply_show_check_procedure(
        drones_user,
        family_user,
        export_report.show_check_report,
        parameter,
    )
    export_report.json_creation_report = JsonCreationReport(len(drones_user.drones))
    apply_json_creation_procedure(
        drones_user,
        family_user,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        export_report.json_creation_report,
    )
    export_report.update()
