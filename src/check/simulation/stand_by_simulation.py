from typing import List, Tuple

import numpy as np

from .position_simulation import SimulationInfo


def stand_by_simulation(
    frame_begin: int,
    frame_end: int,
    stand_by_position: Tuple[float, float, float],
) -> List[SimulationInfo]:
    return [
        SimulationInfo(
            frame=frame_begin + frame_index,
            position=np.array(stand_by_position),
            in_air=False,
            in_dance=False,
        )
        for frame_index in range(frame_end - frame_begin)
    ]
