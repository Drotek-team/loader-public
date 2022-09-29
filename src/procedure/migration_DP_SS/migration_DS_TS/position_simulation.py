from typing import List, Tuple

import numpy as np


### TO DO: add an exception if nb_points < 0, generally due to negative height
def linear_interpolation(
    position_begin: Tuple[float, float, float],
    position_end: Tuple[float, float, float],
    nb_points: int,
) -> List[np.ndarray]:
    if nb_points == 0:
        return []

    return [
        np.round(
            np.array(position_begin) * (1 - percentile)
            + np.array(position_end) * percentile,
            2,
        )
        for percentile in np.linspace(
            0,
            1,
            nb_points,
            endpoint=False,
        )
    ]
