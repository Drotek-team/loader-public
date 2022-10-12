from typing import Tuple
from ...parameter.parameter import FrameParameter
from ...show_trajectory.show_trajectory import TrajectoryInfo
import numpy as np
from typing import List


def stand_by_simulation(
    frame_begin: int,
    frame_end: int,
    stand_by_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
) -> List[TrajectoryInfo]:
    nb_element = int((frame_end - frame_begin) // frame_parameter.position_rate_frame)
    return [
        TrajectoryInfo(np.array(stand_by_position), False, False)
        for _ in range(nb_element)
    ]
