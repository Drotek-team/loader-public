from typing import Tuple

from ....parameter.parameter import FrameParameter
from ....show_simulation.trajectory_simulation import (
    TrajectorySimulation,
)


def stand_by_simulation(
    frame_begin: int,
    frame_end: int,
    stand_by_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
) -> TrajectorySimulation:
    nb_element = int((frame_end - frame_begin) // frame_parameter.position_rate_frame)
    return TrajectorySimulation(
        nb_element * [stand_by_position],
        nb_element * [False],
        nb_element * [False],
    )
