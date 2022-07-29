import numpy as np

from ....drones_manager.drones_manager import DronesManager
from ....family_manager.family_manager import FamilyManager
from ....parameter.parameter import FamilyParameter
from .family_manager_check_report import (
    FamilyManagerCheckReport,
    TheoricalCoherenceCheckReport,
)
from typing import List, Tuple


def family_format_check(family_manager: FamilyManager):
    nb_x_validation = isinstance(family_manager.nb_x, int)
    nb_y_validation = isinstance(family_manager.nb_y, int)
    step_takeoff_validation = isinstance(family_manager.step_takeoff, int)
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
    first_positions: List[Tuple],
    theorical_coherence_check_report: TheoricalCoherenceCheckReport,
) -> None:
    ROW_ALIGNED_TOLERANCE = 1e-6
    if len(first_positions) != len(family_manager.theorical_grid):
        theorical_coherence_check_report.nb_drone_theorical_coherence_check_report.update_report(
            len(first_positions), family_manager.theorical_grid.size
        )
        return
    theorical_coherence_check_report.nb_drone_theorical_coherence_check_report.validation = (
        True
    )
    if (
        np.max(np.array(first_positions) - family_manager.theorical_grid)
        > ROW_ALIGNED_TOLERANCE
    ):
        theorical_coherence_check_report.position_theorical_coherence_check_report.update_report(
            np.max(np.array(first_positions) - family_manager.theorical_grid)
        )
        return
    theorical_coherence_check_report.position_theorical_coherence_check_report.validation = (
        True
    )
    theorical_coherence_check_report.update()


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
    positions_theorical_coherence_check(
        family_manager,
        drones_manager.first_horizontal_positions,
        family_manager_check_report.theorical_coherence_check_report,
    )
    family_manager_check_report.update()
