import numpy as np
import numpy.typing as npt

from .collision_math import (
    get_border_indices,
    get_optimized_collision_infractions,
    get_principal_axis,
    get_unique_list_from_list,
)


def get_numpy_grid(nb_x: int, nb_y: int) -> npt.NDArray[np.float64]:
    return np.array(
        [(index_x, index_y, 0) for index_x in range(nb_x) for index_y in range(nb_y)]
    )


def test_get_principal_axis_x_axis():
    position_numpy = get_numpy_grid(2, 5)
    assert np.array_equal(get_principal_axis(position_numpy), np.array([0, 1, 0]))


def test_get_principal_axis_y_axis():
    positions_numpy = get_numpy_grid(5, 2)
    assert np.array_equal(get_principal_axis(positions_numpy), np.array([1, 0, 0]))


def test_get_border_indices():
    assert np.array_equal(
        get_border_indices(np.array(list(range(10))), 1.5),
        np.array([4, 5, 6]),
    )


def test_get_unique_list_from_list_unique():
    collision_infraction_1 = 0
    collision_infraction_2 = 1
    assert (
        len(get_unique_list_from_list([collision_infraction_1, collision_infraction_2]))
        == 2
    )


def test_get_unique_list_from_list_non_unique():
    collision_infraction_1 = 1
    collision_infraction_2 = 1
    assert (
        len(get_unique_list_from_list([collision_infraction_1, collision_infraction_2]))
        == 1
    )


def test_get_optimized_collision_infractions():
    nb_x, nb_y = 2, 2
    local_indices = np.arange(0, nb_x * nb_y)
    assert len(
        get_optimized_collision_infractions(
            local_indices,
            get_numpy_grid(nb_x, nb_y),
            endangered_distance=1.2,
            in_air=True,
        )
    ) == (nb_x - 1) * nb_y + nb_x * (nb_y - 1)


# TODO: the optimized collision does not work at all, repair it
# It is neutralized for the moment
def test_get_optimized_collision_infractions_big_number():
    nb_x, nb_y = 16, 20
    local_indices = np.arange(0, nb_x * nb_y)
    normal_value = (nb_x - 1) * nb_y + nb_x * (nb_y - 1)
    assert (
        len(
            get_optimized_collision_infractions(
                local_indices,
                get_numpy_grid(nb_x, nb_y),
                endangered_distance=1.2,
                in_air=True,
            )
        )
        == normal_value
    )
