from ...drones_px4.drones_px4 import DronesPx4
from ...show_user.show_user import FamilyUser
from ...parameter.parameter import (
    FamilyParameter,
    FrameParameter,
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
    drones_px4: DronesPx4,
    family_user: FamilyUser,
    frame_parameter: FrameParameter,
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
        drones_px4,
        family_user,
        frame_parameter,
        family_user_check_report.family_user_logic_check_report,
    )
    family_user_check_report.update()