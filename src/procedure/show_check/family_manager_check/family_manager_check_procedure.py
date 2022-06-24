import numpy as np

from ....drones_manager.drones_manager import DronesManager
from ....family_manager.family_manager import FamilyManager
from .family_manager_check_report import FamilyManagerCheckReport


def family_values_check(
    family_manager: FamilyManager,
    family_parameter:FamilyParameter,
) -> bool:
    nb_x_validation = < family_manager.nb_x and 
    return nb_x_validation


def positions_theorical_coherence_check(
    family_manager: FamilyManager,
    ordered_positions: np.ndarray,
) -> bool:
    ROW_ALIGNED_TOLERANCE = 1e-6
    return (
        np.linalg.norm(ordered_positions - family_manager.theorical_grid())
        < ROW_ALIGNED_TOLERANCE
    )


def apply_family_check_procedure(
    drones_manager: DronesManager,
    family_manager: FamilyManager,
    family_manager_check_report: FamilyManagerCheckReport,
    family_parameter:FamilyParameter,
) -> None:
    family_manager_check_report.family_manager_values_check_report = (
        family_values_check(
            family_manager_check_report.family_manager_values_check_report
        )
    )
    family_manager_check_report.positions_theorical_coherence_check_report.validation = positions_theorical_coherence_check(
        family_manager, np.array(drones_manager.first_horizontal_positions())
    )
    family_manager_check_report.update()
