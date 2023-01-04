from typing import List, Tuple

import numpy as np

from .position_simulation import SimulationInfo


def stand_by_simulation(
    frame_begin: int,
    frame_end: int,
    stand_by_position: Tuple[float, float, float],
) -> List[SimulationInfo]:
    if not (isinstance(frame_begin, int)) or not (isinstance(frame_end, int)):
        raise ValueError(frame_begin, frame_end)
    return [
        SimulationInfo(
            frame_begin + frame_index, np.array(stand_by_position), False, False
        )
        for frame_index in range(frame_end - frame_begin)
    ]
