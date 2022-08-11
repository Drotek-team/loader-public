from .....family_manager.family_manager import FamilyManager
from .family_manager_value_check_report import FamilyManagerValueCheckReport
from .....parameter.parameter import FamilyParameter


def apply_family_manager_value_check(
    family_manager: FamilyManager,
    family_parameter: FamilyParameter,
    family_manager_value_check_report: FamilyManagerValueCheckReport,
) -> None:
    family_manager_value_check_report.nbx_value_check_report.validation = (
        family_parameter.nb_x_value_min <= family_manager.nb_x
        and family_manager.nb_x <= family_parameter.nb_x_value_max
    )
    family_manager_value_check_report.nby_value_check_report.validation = (
        family_parameter.nb_x_value_min <= family_manager.nb_x
        and family_manager.nb_x <= family_parameter.nb_x_value_max
    )
    family_manager_value_check_report.step_value_check_report.validation = (
        family_parameter.nb_x_value_min <= family_manager.nb_x
        and family_manager.nb_x <= family_parameter.nb_x_value_max
    )
    family_manager_value_check_report.takeoff_angle_value_check_report.validation = (
        family_parameter.nb_x_value_min <= family_manager.nb_x
        and family_manager.nb_x <= family_parameter.nb_x_value_max
    )
