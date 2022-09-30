from .show_check_report import ShowCheckReport
from ..drones_px4.drones_px4 import DronesPx4
from ..parameter.parameter import Parameter
from .export_report import ExportReport
from .migration_IJ_DP.DP_to_IJ_procedure import DP_to_IJ_procedure
from .show_check_procedure import apply_show_check_procedure
from typing import Dict
from ..show_user.show_user import FamilyUser
from ..show_user.show_user import ShowUser
from .migration_DP_DU.DU_to_DP_procedure import DU_to_DP_procedure


def apply_export_procedure(
    show_user_json: Dict,
    family_user: FamilyUser,
    export_report: ExportReport,
    parameter: Parameter,
) -> None:
    show_user = ShowUser(**show_user_json)
    drones_px4 = DU_to_DP_procedure(show_user.drones_user)
    export_report.show_check_report = ShowCheckReport(len(drones_px4.drones))
    apply_show_check_procedure(
        drones_px4,
        family_user,
        export_report.show_check_report,
        parameter,
    )
    DP_to_IJ_procedure(
        drones_px4,
        family_user,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
    )
    export_report.update()
