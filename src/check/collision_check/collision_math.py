from typing import Any, List

import numpy as np

from ...report.report import CollisionInfraction

ARBITRARY_DICHOTOMY_THRESHOLD = 400_000


def get_couple_distance_matrix(
    positions_numpy: Any,
) -> Any:
    config_matrix = np.tril(1e8 * np.ones((len(positions_numpy), len(positions_numpy))))
    return config_matrix + np.linalg.norm(
        positions_numpy[:, None, :] - positions_numpy[None, :, :], axis=-1
    )


def get_collision_infractions(
    frame: int,
    local_drone_indices: Any,
    local_drone_positions: Any,
    endangered_distance: float,
    *,
    in_air: bool,
) -> List[CollisionInfraction]:
    nb_drones_local = len(local_drone_indices)
    couples_distance_matrix_indices = np.array(
        list(range(nb_drones_local * nb_drones_local))
    )
    couple_distance_matrix = get_couple_distance_matrix(local_drone_positions).reshape(
        nb_drones_local * nb_drones_local,
    )
    endangered_couples_distance_matrix_indices = couples_distance_matrix_indices[
        (couple_distance_matrix < endangered_distance)
    ]
    return [
        CollisionInfraction(
            name=f"Collision Infraction between {endangered_couples_distance_matrix_index}",
            frame=frame,
            drone_index_1=int(
                local_drone_indices[
                    endangered_couples_distance_matrix_index // nb_drones_local
                ]
            ),
            drone_index_2=int(
                local_drone_indices[
                    endangered_couples_distance_matrix_index % nb_drones_local
                ]
            ),
            distance=float(
                couple_distance_matrix[endangered_couples_distance_matrix_index]
            ),
            in_air=in_air,
        )
        for (
            endangered_couples_distance_matrix_index
        ) in endangered_couples_distance_matrix_indices
    ]


def get_principal_axis(
    positions_numpy: Any,
) -> Any:
    x_meaned = positions_numpy - np.mean(positions_numpy, axis=0)
    cov_mat = np.cov(x_meaned, rowvar=False)
    eigen_values, eigen_vectors = np.linalg.eigh(cov_mat)
    return eigen_vectors[:, np.argsort(eigen_values)[-1]]


def get_border_indices(sorted_positions_numpy: Any, endangered_distance: float) -> Any:
    middle_position_numpy = sorted_positions_numpy[len(sorted_positions_numpy) // 2]
    return np.arange(
        np.searchsorted(
            sorted_positions_numpy,
            middle_position_numpy - endangered_distance,
            side="left",
        ),
        np.searchsorted(
            sorted_positions_numpy,
            middle_position_numpy + endangered_distance,
            side="right",
        ),
    )


def get_unique_list_from_list(non_unique_list: List[Any]) -> List[Any]:
    return list(set(non_unique_list))


def get_optimized_collision_infractions(
    frame: int,
    local_indices: Any,
    local_positions_numpy: Any,
    endangered_distance: float,
    *,
    in_air: bool,
) -> List[CollisionInfraction]:
    nb_drones_local = len(local_indices)
    half_nb_drones_local = len(local_indices) // 2
    if nb_drones_local < ARBITRARY_DICHOTOMY_THRESHOLD:
        return get_collision_infractions(
            frame,
            local_indices,
            local_positions_numpy,
            endangered_distance,
            in_air=in_air,
        )
    principal_axis = get_principal_axis(local_positions_numpy)
    argsort_by_axis_positions_numpy = np.argsort(local_positions_numpy @ principal_axis)
    border_indices = get_border_indices(
        local_positions_numpy @ principal_axis, endangered_distance
    )
    return get_unique_list_from_list(
        get_optimized_collision_infractions(
            frame,
            local_indices[argsort_by_axis_positions_numpy[:half_nb_drones_local]],
            local_positions_numpy[
                argsort_by_axis_positions_numpy[:half_nb_drones_local]
            ],
            endangered_distance,
            in_air=in_air,
        )
        + get_optimized_collision_infractions(
            frame,
            local_indices[argsort_by_axis_positions_numpy[half_nb_drones_local:]],
            local_positions_numpy[
                argsort_by_axis_positions_numpy[half_nb_drones_local:]
            ],
            endangered_distance,
            in_air=in_air,
        )
        + get_optimized_collision_infractions(
            frame,
            local_indices[argsort_by_axis_positions_numpy[border_indices]],
            local_positions_numpy[argsort_by_axis_positions_numpy[border_indices]],
            endangered_distance,
            in_air=in_air,
        )
    )
