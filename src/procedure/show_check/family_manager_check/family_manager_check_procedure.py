import numpy as np

from ....drones_manager.drones_manager import DronesManager
from ....family_manager.family_manager import FamilyManager
from ....parameter.parameter import FamilyParameter
from .family_manager_check_report import FamilyManagerCheckReport


def family_format_check(family_manager: FamilyManager):
    nb_x_validation = isinstance(family_manager.nb_x, int)
    nb_y_validation = isinstance(family_manager.nb_y, int)
    step_takeoff_validation = isinstance(family_manager.step_takeoff, float)
    angle_takeoff_validation = isinstance(family_manager.angle_takeoff, int)
    return (
        nb_x_validation
        and nb_y_validation
        and step_takeoff_validation
        and angle_takeoff_validation
    )


def family_value_check(
    family_manager: FamilyManager,
    family_parameter: FamilyParameter,
) -> bool:
    nb_x_validation = (
        family_parameter.nb_x_value_min <= family_manager.nb_x
        and family_manager.nb_x <= family_parameter.nb_x_value_max
    )
    nb_y_validation = (
        family_parameter.nb_y_value_min <= family_manager.nb_y
        and family_manager.nb_y <= family_parameter.nb_y_value_max
    )
    step_takeoff_validation = (
        family_parameter.step_takeoff_value_min <= family_manager.step_takeoff
        and family_manager.step_takeoff <= family_parameter.step_takeoff_value_max
    )
    angle_takeoff_validation = (
        family_parameter.angle_takeoff_value_min <= family_manager.angle_takeoff
        and family_manager.angle_takeoff <= family_parameter.angle_takeoff_value_max
    )
    return (
        nb_x_validation
        and nb_y_validation
        and step_takeoff_validation
        and angle_takeoff_validation
    )


def positions_theorical_coherence_check(
    family_manager: FamilyManager,
    first_positions: np.ndarray,
) -> bool:
    ROW_ALIGNED_TOLERANCE = 1e-3
    return (
        np.linalg.norm(first_positions - family_manager.theorical_grid)
        < ROW_ALIGNED_TOLERANCE
    )


def apply_family_check_procedure(
    drones_manager: DronesManager,
    family_manager: FamilyManager,
    family_parameter: FamilyParameter,
    family_manager_check_report: FamilyManagerCheckReport,
) -> None:
    family_manager_check_report.family_manager_format_check_report.validation = (
        family_format_check(family_manager)
    )
    family_manager_check_report.family_manager_value_check_report.validation = (
        family_value_check(family_manager, family_parameter)
    )
    family_manager_check_report.positions_theorical_coherence_check_report.validation = positions_theorical_coherence_check(
        family_manager, np.array(drones_manager.first_horizontal_positions)
    )
    family_manager_check_report.update()
