from .show_check_report import ShowCheckReport
from ..parameter.parameter import Parameter
from .export_report import ExportReport
from .migration_IJ_DP.DP_to_IJ_procedure import DP_to_IJ_procedure
from .show_check_procedure import apply_show_check_procedure
from typing import Dict
from ..show_user.show_user import ShowUser
from .migration_SP_SU.DU_to_DP_procedure import DU_to_DP_procedure


def apply_export_procedure(
    show_user_json: Dict,
    export_report: ExportReport,
    parameter: Parameter,
) -> None:
    show_user = ShowUser(**show_user_json)
    show_px4 = DU_to_DP_procedure(show_user.drones_user)
    export_report.show_check_report = ShowCheckReport(len(show_px4))
    apply_show_check_procedure(
        show_px4,
        export_report.show_check_report,
        parameter,
    )
    DP_to_IJ_procedure(
        show_px4,
        parameter.json_binary_parameter,
    )
    export_report.update()
