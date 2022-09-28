from .....family_manager.family_manager import FamilyUser
from .family_manager_format_check_report import FamilyUserFormatCheckReport


def apply_family_manager_format_check(
    family_manager: FamilyUser,
    family_manager_format_check_report: FamilyUserFormatCheckReport,
) -> None:
    family_manager_format_check_report.nb_x_format_check_report.validation = isinstance(
        family_manager.nb_x, int
    )
    family_manager_format_check_report.nb_y_format_check_report.validation = isinstance(
        family_manager.nb_y, int
    )
    family_manager_format_check_report.step_format_check_report.validation = isinstance(
        family_manager.step_takeoff, int
    )
    family_manager_format_check_report.takeoff_angle_format_check_report.validation = (
        isinstance(family_manager.angle_takeoff, int)
    )
    family_manager_format_check_report.update()
