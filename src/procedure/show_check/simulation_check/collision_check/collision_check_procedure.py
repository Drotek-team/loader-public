from typing import List

import numpy as np

from .....parameter.parameter import IostarParameter
from .....show_simulation.show_simulation import ShowSimulation
from .collision_check_report import CollisionCheckReport, CollisionInfraction


def get_couple_distance_matrix(positions_numpy: np.ndarray) -> np.ndarray:
    config_matrix = np.tril(1e8 * np.ones((len(positions_numpy), len(positions_numpy))))
    print(config_matrix)
    return config_matrix + np.linalg.norm(
        positions_numpy[:, None, :] - positions_numpy[None, :, :], axis=-1
    )


def get_collision_infractions(
    local_drone_indices: np.ndarray,
    local_drone_positions: np.ndarray,
    in_air: bool,
    endangered_distance: float,
) -> List[CollisionInfraction]:
    nb_drones_local = len(local_drone_indices)
    couples_distance_matrix_indices = np.array(
        [
            column_index * nb_drones_local + row_index
            for column_index in range(nb_drones_local)
            for row_index in range(nb_drones_local)
        ]
    )
    couple_distance_matrix = get_couple_distance_matrix(local_drone_positions).reshape(
        nb_drones_local * nb_drones_local,
    )
    endangered_couples_distance_matrix_indices = couples_distance_matrix_indices[
        (couple_distance_matrix < endangered_distance)
    ]
    return [
        CollisionInfraction(
            local_drone_indices[
                endangered_couples_distance_matrix_index // nb_drones_local
            ],
            local_drone_indices[
                endangered_couples_distance_matrix_index % nb_drones_local
            ],
            in_air,
            couple_distance_matrix[endangered_couples_distance_matrix_index],
        )
        for (
            endangered_couples_distance_matrix_index
        ) in endangered_couples_distance_matrix_indices
    ]


def apply_collision_check_procedure(
    show_simulation: ShowSimulation,
    collision_check_report: CollisionCheckReport,
    iostar_parameter: IostarParameter,
) -> None:
    drone_indices = np.array(range(show_simulation.nb_drones))
    for show_simulation_slice, collision_slice_check_report in zip(
        show_simulation.show_slices,
        collision_check_report.collision_slices_check_report,
    ):
        on_ground_collision_infractions = get_collision_infractions(
            drone_indices[np.invert(show_simulation_slice.in_air_flags)],
            show_simulation_slice.positions[
                np.invert(show_simulation_slice.in_air_flags)
            ],
            False,
            iostar_parameter.security_distance_on_ground,
        )
        in_air_collision_infractions = get_collision_infractions(
            drone_indices[show_simulation_slice.in_air_flags],
            show_simulation_slice.positions[show_simulation_slice.in_air_flags],
            True,
            iostar_parameter.security_distance_in_air,
        )
        collision_slice_check_report.collision_infractions += (
            on_ground_collision_infractions + in_air_collision_infractions
        )
        collision_slice_check_report.update()
    collision_check_report.update()
