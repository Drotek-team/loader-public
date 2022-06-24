from typing import List, Tuple

import numpy as np

from .....parameter.parameter import IostarParameter
from .....show_simulation.show_simulation import ShowSimulation, ShowSimulationSlice
from .collision_check_report import CollisionCheckReport


def couple_distance_matrix(positions_numpy: np.ndarray) -> np.ndarray:
    return 1e8 * np.identity(len(positions_numpy)) + np.linalg.norm(
        positions_numpy[:, None, :] - positions_numpy[None, :, :], axis=-1
    )


def endangered_couples_from_couple_distance_matrix(
    couple_distance_matrix: np.ndarray, endangered_distance: float
) -> np.ndarray:
    return couple_distance_matrix < endangered_distance


def get_endangered_indices(
    drone_positions: np.ndarray,
    drone_indices: np.ndarray,
    endangered_distance: float,
) -> List[Tuple[int, int]]:
    return drone_indices[couple_distance_matrix(drone_positions) < endangered_distance]


def apply_collision_check_procedure(
    show_simulation: ShowSimulation,
    drones_collision_check_report: CollisionCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    drone_indices = range(len(show_simulation.nb_drones))
    for show_simulation_slice in show_simulation.slices.values():
        endangered_drone_on_ground_indices = get_endangered_indices(
            show_simulation_slice.positions,
            drone_indices[np.invert(show_simulation_slice.in_air_flags)],
            iostar_parameter.security_distance_on_ground,
        )
        drones_collision_check_report.drones_collision_check_report.update_ground_collisions(
            endangered_drone_on_ground_indices
        )
        endangered_drone_in_air_flags = get_endangered_indices(
            show_simulation_slice.positions,
            show_simulation_slice.in_air_flags,
            iostar_parameter.security_distance_in_air,
        )
        drones_collision_check_report.drones_collision_check_report.update_in_air_collisions(
            endangered_drone_in_air_flags
        )
