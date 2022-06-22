from typing import List, Tuple

import numpy as np

from .....parameter.parameter import IostarParameter
from .....show_simulation.show_simulation import ShowSimulation
from .collision_check_report import CollisionCheckReport


def get_proximity_matrix(positions_numpy: np.ndarray) -> np.ndarray:
    return 1e8 * np.identity(len(positions_numpy)) + np.linalg.norm(
        positions_numpy[:, None, :] - positions_numpy[None, :, :], axis=-1
    )


def get_endangered_index(
    positions_numpy: np.ndarray,
    drone_indices: np.ndarray,
    minimal_distance: float,
) -> List[Tuple[int, int]]:

    return drone_indices[get_proximity_matrix(positions_numpy) < minimal_distance]


def apply_collision_check_procedure(
    show_simulation: ShowSimulation,
    iostar_parameter: IostarParameter,
    collision_check_report: CollisionCheckReport,
) -> None:
    for show_simulation_slice in show_simulation.slices.values():
        endangered_drone_on_ground_indices = get_endangered_index(
            show_simulation_slice.positions,
            show_simulation_slice.in_air_indices,
            iostar_parameter.security_distance_on_ground,
        )
        endangered_drone_in_air_indices = get_endangered_index(
            show_simulation_slice.positions,
            show_simulation_slice.in_air_indices,
            iostar_parameter.security_distance_in_air,
        )
        collision_check_report.update(
            endangered_drone_on_ground_indices, endangered_drone_in_air_indices
        )
