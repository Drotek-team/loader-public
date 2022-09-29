from .show_check_report import ShowCheckReport
from ..drones_px4.drones_px4 import DronesPx4
from ..parameter.parameter import Parameter
from .export_report import ExportReport
from .migration_IJ_DP.DP_to_IJ_procedure import apply_json_creation_procedure
from .show_check_procedure import apply_show_check_procedure
from typing import Dict
from ..show_user.show_user import FamilyUser


def apply_export_procedure(
    # : Dict,
    drones_px4: DronesPx4,
    family_user: FamilyUser,
    export_report: ExportReport,
    parameter: Parameter,
) -> None:
    export_report.show_check_report = ShowCheckReport(len(drones_px4.drones))
    apply_show_check_procedure(
        drones_px4,
        family_user,
        export_report.show_check_report,
        parameter,
    )
    apply_json_creation_procedure(
        drones_px4,
        family_user,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
    )
    export_report.update()
