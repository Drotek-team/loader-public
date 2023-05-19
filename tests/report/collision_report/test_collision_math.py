from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from loader.reports.collision_report.collision_infraction import (
    CollisionInfraction,
    get_border_indices,
    get_principal_axis,
    get_unique_list_from_list,
)

if TYPE_CHECKING:
    from numpy.typing import NDArray


def get_numpy_grid(nb_x: int, nb_y: int) -> NDArray[np.float64]:
    return np.array(
        [(x, y, 0) for x in range(nb_x) for y in range(nb_y)],
        dtype=np.float64,
    )


def test_get_principal_axis_x_axis() -> None:
    position_numpy = get_numpy_grid(2, 5)
    assert np.array_equal(
        get_principal_axis(position_numpy),
        np.array([0, 1, 0], dtype=np.float64),
    )


def test_get_principal_axis_y_axis() -> None:
    positions_numpy = get_numpy_grid(5, 2)
    assert np.array_equal(
        get_principal_axis(positions_numpy),
        np.array([1, 0, 0], dtype=np.float64),
    )


def test_get_border_indices() -> None:
    assert np.array_equal(
        get_border_indices(np.array(list(range(10)), dtype=np.float64), 1.5),
        np.array([4, 5, 6], dtype=np.float64),
    )


def test_get_unique_list_from_list_unique() -> None:
    collision_infraction_1 = 0
    collision_infraction_2 = 1
    assert len(get_unique_list_from_list([collision_infraction_1, collision_infraction_2])) == 2


def test_get_unique_list_from_list_non_unique() -> None:
    collision_infraction_1 = 1
    collision_infraction_2 = 1
    assert len(get_unique_list_from_list([collision_infraction_1, collision_infraction_2])) == 1


def test_get_optimized_collision_infractions() -> None:
    nb_x, nb_y = 2, 2
    local_indices = np.arange(  # pyright: ignore[reportUnknownMemberType]
        0,
        nb_x * nb_y,
    )
    assert len(
        CollisionInfraction._get_collision_infractions(  # pyright: ignore[reportPrivateUsage]
            0,
            local_indices,
            get_numpy_grid(nb_x, nb_y),
            endangered_distance=1.2,
            in_air=True,
        ),
    ) == (nb_x - 1) * nb_y + nb_x * (nb_y - 1)


# Improve: the optimized collision does not work at all, repair it
# It is neutralized for the moment
def test_get_optimized_collision_infractions_big_number() -> None:
    nb_x, nb_y = 16, 20
    local_indices = np.arange(  # pyright: ignore[reportUnknownMemberType]
        0,
        nb_x * nb_y,
    )
    normal_value = (nb_x - 1) * nb_y + nb_x * (nb_y - 1)
    assert (
        len(
            CollisionInfraction._get_collision_infractions(  # pyright: ignore[reportPrivateUsage]
                0,
                local_indices,
                get_numpy_grid(nb_x, nb_y),
                endangered_distance=1.2,
                in_air=True,
            ),
        )
        == normal_value
    )
