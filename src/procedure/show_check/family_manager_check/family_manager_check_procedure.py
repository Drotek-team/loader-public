from dataclasses import dataclass

import numpy as np

from ....drones_manager.drones_manager import DronesManager
from ....family_manager.family_manager import FamilyManager
from .family_manager_check_report import FamilyManagerCheckReport


@dataclass(frozen=True)
class FamilyCheckParameter:
    ROW_ALIGNED_TOLERANCE: float = 1e-6
    ROW_COLUMN_MINIMAL_DISTANCE: float = 0.75


def check_positions_verticaly_aligned(
    positions_numpy: np.ndarray, family_check_parameter: FamilyCheckParameter
) -> bool:
    proximity_matrix = 1e8 * np.identity(len(positions_numpy)) + np.linalg.norm(
        positions_numpy[:, 1][:, None, :] - positions_numpy[None, :, :],
        axis=-1,
    )
    return np.min(proximity_matrix) > family_check_parameter.ROW_ALIGNED_TOLERANCE


def check_distance_btw_row_valid(
    first_horizontal_positions: np.ndarray,
    second_positions_numpy: np.ndarray,
    family_check_parameter: FamilyCheckParameter,
) -> bool:

    return (
        second_positions_numpy[0] - first_horizontal_positions[0]
        > family_check_parameter.ROW_ALIGNED_TOLERANCE
    )


def check_ordered_positions_first_positions_coherence(
    ordered_positions: np.ndarray,
    positions_numpy: np.ndarray,
) -> bool:
    return ordered_positions == positions_numpy


def check_ordered_positions_verticality_aligned(
    ordered_row_positions: np.ndarray,
    family_check_parameter: FamilyCheckParameter,
) -> bool:
    for row_positions in ordered_row_positions:
        if not (
            check_positions_verticaly_aligned(row_positions, family_check_parameter)
        ):
            return False
    return True


def check_ordered_positions_row_column_distances(
    ordered_row_positions: np.ndarray,
    family_check_parameter: FamilyCheckParameter,
) -> bool:
    for row_index in range(len(ordered_row_positions) - 1):
        if not (
            check_distance_btw_row_valid(
                ordered_row_positions[row_index],
                ordered_row_positions[row_index + 1],
                family_check_parameter,
            )
        ):
            return False
    for row_index in range(len(ordered_row_positions[:, 1]) - 1):
        if not (
            check_distance_btw_row_valid(
                ordered_row_positions[row_index],
                ordered_row_positions[row_index + 1],
                family_check_parameter,
            )
        ):
            return False
    return True


def get_ordered_positions(
    positions_numpy: np.ndarray, family_manager: FamilyManager
) -> np.ndarray:
    sorted_positions = positions_numpy[np.argsort(positions_numpy[:, 1])]
    position_index = 0
    ordered_positions = np.zeros((positions_numpy.shape))
    for row_index in range(len(family_manager.rows)):
        row_positions = sorted_positions[
            position_index : position_index
            + family_manager.get_nb_drone_per_row(row_index)
        ]
        row_positions_sorted = row_positions[np.argsort(positions_numpy[:, 0])]
        position_index += family_manager.get_nb_drone_per_row(row_index)
        ordered_positions[row_index] = row_positions_sorted
    return ordered_positions


def apply_family_check_procedure(
    drones_manager: DronesManager,
    family_manager: FamilyManager,
    family_check_report: FamilyManagerCheckReport,
) -> None:
    family_check_parameter = FamilyCheckParameter()

    ordered_positions = get_ordered_positions(
        drones_manager.get_first_positions(), family_manager
    )
    check_ordered_positions_first_positions_coherence(
        first_horizontal_positions, ordered_positions
    )
    check_ordered_positions_verticality_aligned(
        ordered_positions, family_check_parameter
    )
    check_ordered_positions_row_column_distances(
        ordered_positions, family_check_parameter
    )
