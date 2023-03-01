import os
import sys
from typing import Callable, TypeVar

if sys.version_info < (3, 10):  # pragma: no cover
    from typing_extensions import ParamSpec
else:  # pragma: no cover
    from typing import ParamSpec

import numpy as np
from hypothesis import settings
from hypothesis import strategies as st

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


st_nb_x = st.integers(1, 3)
st_nb_y = st.integers(1, 3)
st_nb_drone_per_family = st.integers(1, 3)
st_step_takeoff = st.floats(1, 10)
st_angle_takeoff = st.floats(0, 2 * np.pi)
