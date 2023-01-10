from typing import Dict, Tuple

from ..check.all_check_from_show_user_procedure import (
    apply_all_check_from_show_user_procedure,
)
from ..check.show_check_report import ShowCheckReport
from ..iostar_json.iostar_json import IostarJson
from ..migration.migration_sp_ij.sp_to_ij_procedure import sp_to_ij_procedure
from ..migration.migration_sp_su.su_to_sp_procedure import su_to_sp_procedure
from ..show_user.show_user import ShowUser


def apply_export_procedure(
    show_user_json: Dict,
) -> Tuple[IostarJson, ShowCheckReport]:
    show_user = ShowUser(**show_user_json)
    show_check_report = ShowCheckReport(len(show_user.drones_user))
    apply_all_check_from_show_user_procedure(show_user, show_check_report)
    return (
        sp_to_ij_procedure(su_to_sp_procedure(show_user)),
        show_check_report,
    )
