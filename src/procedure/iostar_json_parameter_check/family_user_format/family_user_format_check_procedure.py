from ....show_user.show_user import FamilyUser

from .family_user_format_check_report import FamilyUserFormatCheckReport


def apply_family_user_format_check(
    family_user: FamilyUser,
    family_user_format_check_report: FamilyUserFormatCheckReport,
) -> None:
    family_user_format_check_report.nb_x_format_check_report.validation = isinstance(
        family_user.nb_x, int
    )
    family_user_format_check_report.nb_y_format_check_report.validation = isinstance(
        family_user.nb_y, int
    )
    family_user_format_check_report.step_format_check_report.validation = isinstance(
        family_user.step_takeoff, float
    )
    family_user_format_check_report.takeoff_angle_format_check_report.validation = (
        isinstance(family_user.angle_takeoff, int)
    )
    family_user_format_check_report.update()
