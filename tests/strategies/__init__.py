import os
from collections.abc import Callable
from typing import TYPE_CHECKING, ParamSpec, TypeVar, cast

import numpy as np
from hypothesis import assume, settings
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays  # pyright: ignore[reportUnknownVariableType]
from loader.parameters.json_binary_parameters import LandType, MagicNumber

if TYPE_CHECKING:
    from numpy.typing import NDArray


P = ParamSpec("P")
T = TypeVar("T")


def slow(func: Callable[P, T]) -> Callable[P, T]:  # pragma: no cover
    """Limit the number of examples for slow tests.

    Setting the environment variable HYPOTHESIS_SLOW to any value will
    disable this decorator.
    """
    if os.environ.get("HYPOTHESIS_SLOW"):
        return func
    return settings(max_examples=10)(func)


@st.composite
def st_matrix(draw: st.DrawFn) -> "NDArray[np.intp]":
    return draw(st_matrix_with_shape())[0]


@st.composite
def st_matrix_with_shape(draw: st.DrawFn) -> tuple["NDArray[np.intp]", int, int, int]:
    nb_x = draw(st.integers(1, 3))
    nb_y = draw(st.integers(1, 3))
    st_nb_drones_per_family = st.integers(0, 3)
    matrix = draw(
        cast(
            st.SearchStrategy["NDArray[np.intp]"],
            arrays(
                np.intp,
                (nb_y, nb_x),
                elements=st_nb_drones_per_family,
            ),
        ),
    )
    assume(matrix[0, :].sum() > 0)
    assume(matrix[-1, :].sum() > 0)
    assume(matrix[:, 0].sum() > 0)
    assume(matrix[:, -1].sum() > 0)
    return matrix, nb_x, nb_y, matrix.max()


st_step_takeoff = st.floats(1, 10)
st_angle_takeoff = st.floats(0, 2 * np.pi)
st_scale = st.integers(1, 4)
st_land_type = st.sampled_from(LandType)
st_magic_number = st.sampled_from(MagicNumber)
