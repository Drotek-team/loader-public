from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import numpy.typing as npt


@dataclass(frozen=True)
class SimulationInfo:
    frame: int
    position: npt.NDArray[np.float64]
    in_air: bool
    in_dance: bool

    def __eq__(self, other_simulation_info: "SimulationInfo"):
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
) -> List[npt.NDArray[np.float64]]:
    if nb_points < 0:
        msg = f"nb_points must be positive: position_begin: {position_begin}, position_end: {position_end}, nb_points: {nb_points}"
        raise ValueError(msg)
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
