from typing import Dict, Tuple

from ..check.all_check_from_show_px4_procedure import (
    apply_all_check_from_show_px4_procedure,
)
from ..check.show_check_report import ShowCheckReport
from ..iostar_json.iostar_json import IostarJson
from ..migration.migration_IJ_SP.IJ_to_SP_procedure import IJ_to_SP_procedure
from ..migration.migration_IJ_SP.IJ_to_SP_report import IJ_to_SP_report
from ..migration.migration_SP_SU.SP_to_SU_procedure import SP_to_SU_procedure
from ..parameter.parameter import Parameter
from ..show_user.show_user import ShowUser


def apply_import_procedure(
    iostar_json_dict: Dict,
    parameter: Parameter,
) -> Tuple[ShowUser, ShowCheckReport]:
    iostar_json = IostarJson(**iostar_json_dict)
    json_extraction_report = IJ_to_SP_report()
    show_px4 = IJ_to_SP_procedure(
        iostar_json,
        parameter.iostar_parameter,
        parameter.json_binary_parameter,
        json_extraction_report,
    )
    show_check_report = apply_all_check_from_show_px4_procedure(
        show_px4,
        parameter,
    )
    return SP_to_SU_procedure(show_px4, parameter.frame_parameter), show_check_report
