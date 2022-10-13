from typing import Tuple
from ....parameter.parameter import FrameParameter
import numpy as np
from typing import List
from .position_simulation import SimulationInfo


def stand_by_simulation(
    frame_begin: int,
    frame_end: int,
    stand_by_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
) -> List[SimulationInfo]:
    nb_element = int((frame_end - frame_begin) // frame_parameter.position_rate_frame)
    return [
        SimulationInfo(np.array(stand_by_position), False, False)
        for _ in range(nb_element)
    ]
