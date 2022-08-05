from typing import Tuple

from ...parameter.parameter import FrameParameter
from .dance_simulation import DanceSequence


def stand_by_simulation(
    frame_begin: int,
    frame_end: int,
    stand_by_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
) -> DanceSequence:
    nb_element = int((frame_end - frame_begin) // frame_parameter.position_rate_frame)
    return DanceSequence(
        nb_element * [stand_by_position],
        nb_element * [False],
        nb_element * [False],
    )
