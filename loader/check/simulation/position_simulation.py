from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from numpy.typing import NDArray


@dataclass(frozen=True)
class SimulationInfo:
    frame: int
    position: NDArray[np.float64]
    in_air: bool

    def __eq__(self, other_simulation_info: object) -> bool:
        if not isinstance(other_simulation_info, SimulationInfo):
            return False
        return bool(
            self.frame == other_simulation_info.frame
            and np.array_equal(self.position, other_simulation_info.position)
            and self.in_air == other_simulation_info.in_air,
        )


def linear_interpolation(
    position_begin: tuple[float, float, float],
    position_end: tuple[float, float, float],
    nb_points: int,
) -> list[NDArray[np.float64]]:
    if nb_points < 0:
        msg = f"nb_points must be positive: position_begin: {position_begin}, position_end: {position_end}, nb_points: {nb_points}"
        raise ValueError(msg)
    if nb_points == 0:
        return []
    return [
        np.round(  # pyright: ignore[reportUnknownMemberType]
            np.array(position_begin, dtype=np.float64) * (1 - percentile)
            + np.array(position_end, dtype=np.float64) * percentile,
            3,
        )
        for percentile in np.linspace(
            0,
            1,
            nb_points,
            endpoint=False,
        )
    ]
