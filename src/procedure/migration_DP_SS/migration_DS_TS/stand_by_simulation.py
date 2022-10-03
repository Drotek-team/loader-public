from typing import Tuple

from ....parameter.parameter import FrameParameter
from ....show_simulation.trajectory_simulation import (
    TrajectorySimulation,
)
import numpy as np


def stand_by_simulation(
    frame_begin: int,
    frame_end: int,
    stand_by_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
) -> TrajectorySimulation:
    nb_element = int((frame_end - frame_begin) // frame_parameter.position_rate_frame)
    return TrajectorySimulation(
        [np.array(stand_by_position) for _ in range(nb_element)],
        [False for _ in range(nb_element)],
        [False for _ in range(nb_element)],
    )
