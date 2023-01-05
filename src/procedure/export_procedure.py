from typing import Dict, Tuple

from ..check.all_check_from_show_px4_procedure import (
    apply_all_check_from_show_user_procedure,
)
from ..check.show_check_report import ShowCheckReport
from ..iostar_json.iostar_json import IostarJson
from ..show_user.show_user import ShowUser


def apply_export_procedure(
    show_user_json: Dict,
) -> Tuple[IostarJson, ShowCheckReport]:
    show_user = ShowUser(**show_user_json)
    show_check_report = apply_all_check_from_show_user_procedure(
        show_user,
    )
    return (
        SU_to_IJ_procedure(show_user),
        show_check_report,
    )
