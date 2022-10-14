from .show_check_report import ShowCheckReport
from ..parameter.parameter import Parameter
from ..migration.migration_IJ_SP.SP_to_IJ_procedure import SP_to_IJ_procedure
from .all_check_from_show_px4_procedure import apply_all_check_from_show_px4_procedure
from typing import Dict, Tuple
from ..show_user.show_user import ShowUser
from ..migration.migration_SP_SU.SU_to_SP_procedure import SU_to_SP_procedure
from ..iostar_json.iostar_json import IostarJson


def apply_export_procedure(
    show_user_json: Dict,
    parameter: Parameter,
) -> Tuple[IostarJson, ShowCheckReport]:
    show_user = ShowUser(**show_user_json)
    show_px4 = SU_to_SP_procedure(show_user)
    show_check_report = apply_all_check_from_show_px4_procedure(
        show_px4,
        parameter,
    )
    SP_to_IJ_procedure(
        show_px4,
        parameter.json_binary_parameter,
    )
    return (
        SP_to_IJ_procedure(show_px4, parameter.json_binary_parameter),
        show_check_report,
    )
