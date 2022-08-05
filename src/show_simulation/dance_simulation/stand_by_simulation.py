from typing import Tuple

from ...parameter.parameter import FrameParameter
from .dance_simulation import DanceSequence


def stand_by_simulation(
    second_begin: float,
    second_end: float,
    stand_by_position: Tuple[float, float, float],
    frame_parameter: FrameParameter,
) -> DanceSequence:
    nb_element = int((second_end - second_begin) / frame_parameter.position_second_rate)
    return DanceSequence(
        nb_element * [stand_by_position],
        nb_element * [False],
        nb_element * [False],
    )
