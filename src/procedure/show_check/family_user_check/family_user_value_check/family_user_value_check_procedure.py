from .....family_user.family_user import FamilyUser
from .family_user_value_check_report import FamilyUserValueCheckReport
from .....parameter.parameter import FamilyParameter


def apply_family_user_value_check(
    family_user: FamilyUser,
    family_parameter: FamilyParameter,
    family_user_value_check_report: FamilyUserValueCheckReport,
) -> None:
    family_user_value_check_report.nb_x_value_check_report.validation = (
        family_parameter.nb_x_value_min <= family_user.nb_x
        and family_user.nb_x <= family_parameter.nb_x_value_max
    )
    family_user_value_check_report.nb_y_value_check_report.validation = (
        family_parameter.nb_y_value_min <= family_user.nb_y
        and family_user.nb_y <= family_parameter.nb_y_value_max
    )
    family_user_value_check_report.step_value_check_report.validation = (
        family_parameter.step_takeoff_value_min <= family_user.step_takeoff
        and family_user.step_takeoff <= family_parameter.step_takeoff_value_max
    )
    family_user_value_check_report.takeoff_angle_value_check_report.validation = (
        family_parameter.angle_takeoff_value_min <= family_user.angle_takeoff
        and family_user.angle_takeoff <= family_parameter.angle_takeoff_value_max
    )
    family_user_value_check_report.update()