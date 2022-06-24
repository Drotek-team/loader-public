from typing import List, Tuple

import numpy as np

from .....parameter.parameter import IostarParameter
from .....show_simulation.show_simulation import ShowSimulation
from .collision_check_report import CollisionCheckReport


def couple_distance_matrix(positions_numpy: np.ndarray) -> np.ndarray:
    return 1e8 * np.identity(len(positions_numpy)) + np.linalg.norm(
        positions_numpy[:, None, :] - positions_numpy[None, :, :], axis=-1
    )


def endangered_couples(
    local_drone_indices: np.ndarray,
    local_drone_positions: np.ndarray,
    endangered_distance: float,
) -> List[Tuple[int, int]]:
    nb_drones_local = len(local_drone_indices)
    couples_distance_matrix_indices = np.array(
        [
            row_index * nb_drones_local + column_index
            for column_index in range(nb_drones_local)
            for row_index in range(nb_drones_local)
        ]
    )
    endangered_couples_distance_matrix_indices = couples_distance_matrix_indices[
        (couple_distance_matrix(local_drone_positions) < endangered_distance).reshape(
            (nb_drones_local * nb_drones_local,)
        )
    ]
    return [
        (
            local_drone_indices[
                endangered_couples_distance_matrix_index // nb_drones_local
            ],
            local_drone_indices[
                endangered_couples_distance_matrix_index % nb_drones_local
            ],
        )
        for endangered_couples_distance_matrix_index in endangered_couples_distance_matrix_indices
    ]


def apply_collision_check_procedure(
    show_simulation: ShowSimulation,
    drones_collision_check_report: CollisionCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    drone_indices = np.array(range(show_simulation.nb_drones))
    for show_simulation_slice in show_simulation.slices:
        drones_collision_check_report.update_collisions_info(
            timecode=show_simulation_slice.timecode,
            endangered_couples=endangered_couples(
                drone_indices[np.invert(show_simulation_slice.in_air_flags)],
                show_simulation_slice.positions[
                    np.invert(show_simulation_slice.in_air_flags)
                ],
                iostar_parameter.security_distance_on_ground,
            ),
            in_air=False,
        )
        drones_collision_check_report.update_collisions_info(
            timecode=show_simulation_slice.timecode,
            endangered_couples=endangered_couples(
                drone_indices[show_simulation_slice.in_air_flags],
                show_simulation_slice.positions[show_simulation_slice.in_air_flags],
                iostar_parameter.security_distance_in_air,
            ),
            in_air=True,
        )
    drones_collision_check_report.update()
