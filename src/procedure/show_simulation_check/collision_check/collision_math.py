from .collision_check_report import CollisionInfraction
import numpy as np
from typing import List


def get_couple_distance_matrix(positions_numpy: np.ndarray) -> np.ndarray:
    config_matrix = np.tril(1e8 * np.ones((len(positions_numpy), len(positions_numpy))))
    return config_matrix + np.linalg.norm(
        positions_numpy[:, None, :] - positions_numpy[None, :, :], axis=-1
    )


### TO DO: not very clean to have two different object for indices and position, better group them in a single class
def get_collision_infractions(
    local_drone_indices: np.ndarray,
    local_drone_positions: np.ndarray,
    in_air: bool,
    endangered_distance: float,
) -> List[CollisionInfraction]:
    nb_drones_local = len(local_drone_indices)
    couples_distance_matrix_indices = np.arange(nb_drones_local * nb_drones_local)
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


def get_principal_axis(positions_numpy: np.ndarray) -> np.ndarray:
    X_meaned = positions_numpy - np.mean(positions_numpy, axis=0)
    cov_mat = np.cov(X_meaned, rowvar=False)
    eigen_values, eigen_vectors = np.linalg.eigh(cov_mat)
    return eigen_vectors[:, np.argsort(eigen_values)[-1]]


def get_border_indices(
    sorted_positions_numpy: np.ndarray, endangered_distance: float
) -> np.ndarray:
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


ARBITRARY_DICHOTOMY_THRESHOLD = 100

### TO DO: not very clean to have two different object for indices and position, better group them in a single class
def get_optimized_collision_infractions(
    local_indices: np.ndarray,
    local_positions_numpy: np.ndarray,
    in_air: bool,
    endangered_distance: float,
) -> List[CollisionInfraction]:
    nb_drones_local = len(local_indices)
    half_nb_drones_local = len(local_indices) // 2
    if nb_drones_local < ARBITRARY_DICHOTOMY_THRESHOLD:
        return get_collision_infractions(
            local_indices, local_positions_numpy, in_air, endangered_distance
        )
    principal_axis = get_principal_axis(local_positions_numpy)
    argsort_by_axis_positions_numpy = np.argsort(local_positions_numpy @ principal_axis)
    border_indices = get_border_indices(
        local_positions_numpy @ principal_axis, endangered_distance
    )
    return (
        get_optimized_collision_infractions(
            local_indices[argsort_by_axis_positions_numpy[:half_nb_drones_local]],
            local_positions_numpy[
                argsort_by_axis_positions_numpy[:half_nb_drones_local]
            ],
            in_air,
            endangered_distance,
        )
        + get_optimized_collision_infractions(
            local_indices[argsort_by_axis_positions_numpy[half_nb_drones_local:]],
            local_positions_numpy[
                argsort_by_axis_positions_numpy[half_nb_drones_local:]
            ],
            in_air,
            endangered_distance,
        )
        + get_optimized_collision_infractions(
            local_indices[argsort_by_axis_positions_numpy[border_indices]],
            local_positions_numpy[argsort_by_axis_positions_numpy[border_indices]],
            in_air,
            endangered_distance,
        )
    )
