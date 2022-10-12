from .collision_math import (
    get_principal_axis,
    get_border_indices,
    get_optimized_collision_infractions,
    get_unique_list_from_list,
)
import numpy as np
from .collision_check_report import CollisionInfraction


def get_grid(nb_x: int, nb_y: int) -> np.ndarray:
    return np.array(
        [(index_x, index_y, 0) for index_x in range(nb_x) for index_y in range(nb_y)]
    )


def test_get_principal_axis_x_axis():
    NB_X = 2
    NB_Y = 5
    POSITIONS_NUMPY = get_grid(NB_X, NB_Y)
    get_principal_axis(POSITIONS_NUMPY)
    assert np.array_equal(get_principal_axis(POSITIONS_NUMPY), np.array([0, 1, 0]))


def test_get_principal_axis_y_axis():
    NB_X = 5
    NB_Y = 2
    POSITIONS_NUMPY = get_grid(NB_X, NB_Y)
    get_principal_axis(POSITIONS_NUMPY)
    assert np.array_equal(get_principal_axis(POSITIONS_NUMPY), np.array([1, 0, 0]))


def test_get_border_indices():
    N = 10
    POSITIONS_NUMPY = np.arange(0, N)
    ENDANGERED_DISTANCE = 1.5
    assert np.array_equal(
        get_border_indices(POSITIONS_NUMPY, ENDANGERED_DISTANCE), np.array([4, 5, 6])
    )


def test_get_unique_list_from_list_unique():
    collision_infraction_1 = CollisionInfraction(0, 1, True, 1.0)
    collision_infraction_2 = CollisionInfraction(0, 2, True, 1.0)
    # raise ValueError()
    assert get_unique_list_from_list(
        [collision_infraction_1, collision_infraction_2]
    ) == [collision_infraction_1, collision_infraction_2]


def test_get_unique_list_from_list_non_unique():
    collision_infraction_1 = CollisionInfraction(0, 1, True, 1.0)
    collision_infraction_2 = CollisionInfraction(0, 1, True, 1.0)
    # raise ValueError()
    assert get_unique_list_from_list(
        [collision_infraction_1, collision_infraction_2]
    ) == [collision_infraction_1]


### TO DO: finished the test
def test_get_optimized_collision_infractions():
    NB_X = 2
    NB_Y = 2
    local_indices = np.arange(0, NB_X * NB_Y)
    # raise ValueError(
    #     get_optimized_collision_infractions(
    #         local_indices, get_grid(NB_X, NB_Y), True, endangered_distance=1.2
    #     )
    # )
    nb_drones_total = NB_X * NB_Y
    assert len(
        get_optimized_collision_infractions(
            local_indices, get_grid(NB_X, NB_Y), True, endangered_distance=1.2
        )
    ) == (NB_X - 1) * NB_Y + NB_X * (NB_Y - 1)


### TO DO: finished the test
def test_get_optimized_collision_infractions_big_number():
    NB_X = 25
    NB_Y = 20

    local_indices = np.arange(0, NB_X * NB_Y)
    assert len(
        get_optimized_collision_infractions(
            local_indices, get_grid(NB_X, NB_Y), True, endangered_distance=1.2
        )
    ) == (NB_X - 1) * NB_Y + NB_X * (NB_Y - 1)
