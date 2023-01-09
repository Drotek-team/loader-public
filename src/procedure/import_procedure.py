from typing import Dict, Tuple

from ..check.show_check_report import ShowCheckReport
from ..show_user.show_user import ShowUser


def apply_import_procedure(
    iostar_json_dict: Dict,
) -> Tuple[ShowUser, ShowCheckReport]:
    pass
    # iostar_json = IostarJson(**iostar_json_dict)
    # json_extraction_report = IJ_to_SP_report()
    # show_px4 = IJ_to_SP_procedure(
    #     iostar_json,
    #     json_extraction_report,
    # )
    # show_user = SP_to_SU_procedure(show_px4)
    # raise ValueError(show_user)
    # show_check_report = apply_all_check_from_show_user_procedure(
    #     show_user,
    # )
    # return show_user, show_check_report
