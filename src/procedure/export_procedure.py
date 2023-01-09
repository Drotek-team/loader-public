from typing import Dict, Tuple

from ..check.all_check_from_show_user_procedure import (
    apply_all_check_from_show_user_procedure,
)
from ..check.show_check_report import ShowCheckReport
from ..iostar_json.iostar_json import IostarJson
from ..migration.migration_SP_IJG.SP_to_IJG_procedure import SP_to_IJG_procedure
from ..migration.migration_SP_SU.SU_to_SP_procedure import SU_to_SP_procedure
from ..show_user.show_user import ShowUser


def apply_export_procedure(
    show_user_json: Dict,
) -> Tuple[IostarJson, ShowCheckReport]:
    show_user = ShowUser(**show_user_json)
    show_check_report = ShowCheckReport(len(show_user.drones_user))
    apply_all_check_from_show_user_procedure(show_user, show_check_report)
    return (
        SP_to_IJG_procedure(SU_to_SP_procedure(show_user)),
        show_check_report,
    )
