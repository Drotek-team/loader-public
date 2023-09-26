import numpy as np
import pytest
from loader.schemas.show_user.show_position_frame.simulation.position_simulation import (
    SimulationInfo,
    linear_interpolation,
)
from numpy.testing import assert_array_equal


def test_get_simulation_info___eq___simulation_info() -> None:
    simulation_info_1 = SimulationInfo(
        frame=0,
        position=np.array([0, 0, 0], dtype=np.float64),
    )
    simulation_info_2 = SimulationInfo(
        frame=0,
        position=np.array([0, 0, 0], dtype=np.float64),
    )
    assert simulation_info_1 == simulation_info_2

    simulation_info_2 = SimulationInfo(
        frame=1,
        position=np.array([0, 0, 0], dtype=np.float64),
    )
    assert simulation_info_1 != simulation_info_2

    simulation_info_2 = SimulationInfo(
        frame=0,
        position=np.array([1, 0, 0], dtype=np.float64),
    )
    assert simulation_info_1 != simulation_info_2


def test_get_simulation_info___eq___not_simulation_info() -> None:
    simulation_info = SimulationInfo(
        frame=0,
        position=np.array([0, 0, 0], dtype=np.float64),
    )
    assert simulation_info != 0


def test_linear_interpolation_standard_case() -> None:
    position_begin = (0, 0, 0)
    position_end = (2, 4, 6)
    nb_points = 4

    assert_array_equal(
        linear_interpolation(position_begin, position_end, nb_points),
        np.array(
            [
                [0, 0, 0],
                [0.5, 1, 1.5],
                [1, 2, 3],
                [1.5, 3, 4.5],
            ],
            dtype=np.float64,
        ),
    )


@pytest.mark.parametrize("nb_points", [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10])
def test_linear_interpolation_invalid_nb_points(nb_points: int) -> None:
    position_begin = (0, 0, 0)
    position_end = (2, 4, 6)

    with pytest.raises(
        ValueError,
        match=f"nb_points must be positive: nb_points = {nb_points}",
    ):
        linear_interpolation(position_begin, position_end, nb_points)
