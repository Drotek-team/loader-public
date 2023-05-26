from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


def get_matrix(*, nb_x: int = 1, nb_y: int = 1, nb_drone_per_family: int = 1) -> "NDArray[np.intp]":
    return np.full((nb_y, nb_x), nb_drone_per_family, dtype=np.intp)
