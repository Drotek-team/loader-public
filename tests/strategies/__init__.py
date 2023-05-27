import os
import sys
from typing import TYPE_CHECKING, Callable, TypeVar, cast

import numpy as np
from hypothesis import assume, settings
from hypothesis import strategies as st
from hypothesis.extra.numpy import arrays  # pyright: ignore[reportUnknownVariableType]

if sys.version_info < (3, 10):  # pragma: no cover
    from typing_extensions import ParamSpec
else:  # pragma: no cover
    from typing import ParamSpec

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
    st_nb_x = st.integers(1, 3)
    st_nb_y = st.integers(1, 3)
    st_nb_drone_per_family = st.integers(0, 3)
    matrix = draw(
        cast(
            st.SearchStrategy["NDArray[np.intp]"],
            arrays(
                np.intp,
                st.tuples(st_nb_x, st_nb_y),
                elements=st_nb_drone_per_family,
            ),
        ),
    )
    assume(matrix.sum() > 0)  # pyright: ignore[reportUnknownMemberType]
    return matrix


st_step_takeoff = st.floats(1, 10)
st_angle_takeoff = st.floats(0, 2 * np.pi)
