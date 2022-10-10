from ...drones_px4.drones_px4 import DronesPx4
from ...show_user.show_user import FamilyUser
from ...parameter.parameter import (
    FamilyUserParameter,
    FrameParameter,
)
from .IJ_param_check_report import (
    FamilyUserCheckReport,
)
from .IJ_param_value_check.IJ_param_value_check_procedure import (
    apply_family_user_value_check,
)
from .IJ_param_logic_check.IJ_param_logic_check_procedure import (
    apply_family_user_logic_check_procedure,
)


def apply_family_check_procedure(
    drones_px4: DronesPx4,
    family_user: FamilyUser,
    frame_parameter: FrameParameter,
    family_user_parameter: FamilyUserParameter,
    family_user_check_report: FamilyUserCheckReport,
) -> None:
    apply_family_user_value_check(
        family_user,
        family_user_parameter,
        family_user_check_report.family_user_value_check_report,
    )
    apply_family_user_logic_check_procedure(
        drones_px4,
        family_user,
        frame_parameter,
        family_user_check_report.family_user_logic_check_report,
    )
    family_user_check_report.update()
