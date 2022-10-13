from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
from typing import Any


@dataclass(frozen=True)
class SimulationInfo:
    frame: int
    position: np.ndarray
    in_air: bool
    in_dance: bool

    def __eq__(self, other_simulation_info: Any):
        return (
            self.frame == other_simulation_info.frame
            and np.array_equal(self.position, other_simulation_info.position)
            and self.in_air == other_simulation_info.in_air
            and self.in_dance == other_simulation_info.in_dance
        )


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
