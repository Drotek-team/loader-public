from dataclasses import dataclass
from typing import List, Tuple
import numpy as np


@dataclass(frozen=True)
class SimulationInfo:
    position: np.ndarray
    in_air: bool
    in_dance: bool


### TO DO: adapt that to new format
def linear_interpolation(
    position_begin: Tuple[float, float, float],
    position_end: Tuple[float, float, float],
    nb_points: int,
    end_point: bool = False,
) -> List[np.ndarray]:
    if nb_points < 0:
        raise ValueError
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
            endpoint=end_point,
        )
    ]
