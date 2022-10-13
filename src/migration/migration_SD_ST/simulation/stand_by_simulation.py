from typing import Tuple
from ....parameter.parameter import FrameParameter
import numpy as np
from typing import List
from .position_simulation import SimulationInfo


def stand_by_simulation(
    frame_begin: int,
    frame_end: int,
    stand_by_position: Tuple[float, float, float],
) -> List[SimulationInfo]:
    return [
        SimulationInfo(
            frame_begin + frame_index, np.array(stand_by_position), False, False
        )
        for frame_index in range(frame_end - frame_begin)
    ]
