from typing import Dict, Tuple

from ..check.all_check_from_show_px4_procedure import (
    apply_all_check_from_show_px4_procedure,
)
from ..check.show_check_report import ShowCheckReport
from ..iostar_json.iostar_json import IostarJson
from ..migration.migration_IJ_SP.SP_to_IJ_procedure import SP_to_IJ_procedure
from ..migration.migration_SP_SU.SU_to_SP_procedure import SU_to_SP_procedure
from ..show_user.show_user import ShowUser


def apply_export_procedure(
    show_user_json: Dict,
) -> Tuple[IostarJson, ShowCheckReport]:
    show_user = ShowUser(**show_user_json)
    show_px4 = SU_to_SP_procedure(show_user)
    show_check_report = apply_all_check_from_show_px4_procedure(
        show_px4,
    )
    SP_to_IJ_procedure(
        show_px4,
    )
    return (
        SP_to_IJ_procedure(show_px4),
        show_check_report,
    )
