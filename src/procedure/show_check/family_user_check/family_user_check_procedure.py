import numpy as np

from ....drones_px4.drones_user import DronesUser
from ....family_user.family_user import FamilyUser
from ....parameter.parameter import (
    FamilyParameter,
    FrameParameter,
    JsonConvertionConstant,
)
from .family_user_check_report import (
    FamilyUserCheckReport,
)
from .family_user_format.family_user_format_check_procedure import (
    apply_family_user_format_check,
)
from .family_user_value_check.family_user_value_check_procedure import (
    apply_family_user_value_check,
)
from .family_user_logic_check.family_user_logic_check_procedure import (
    apply_family_user_logic_check_procedure,
)


def apply_family_check_procedure(
    drones_user: DronesUser,
    family_user: FamilyUser,
    frame_parameter: FrameParameter,
    json_convertion_constant: JsonConvertionConstant,
    family_parameter: FamilyParameter,
    family_user_check_report: FamilyUserCheckReport,
) -> None:
    apply_family_user_format_check(
        family_user, family_user_check_report.family_user_format_check_report
    )
    apply_family_user_value_check(
        family_user,
        family_parameter,
        family_user_check_report.family_user_value_check_report,
    )
    apply_family_user_logic_check_procedure(
        drones_user,
        family_user,
        frame_parameter,
        json_convertion_constant,
        family_user_check_report.family_user_logic_check_report,
    )
    family_user_check_report.update()
