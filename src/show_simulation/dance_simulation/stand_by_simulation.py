from typing import Tuple

from ...parameter.parameter import JsonConvertionConstant, TimecodeParameter
from .dance_simulation import DanceSequence


def stand_by_simulation(
    timecode_begin: int,
    timecode_end: int,
    stand_by_position: Tuple[int, int, int],
    timecode_parameter: TimecodeParameter,
    json_convertion_constant: JsonConvertionConstant,
) -> DanceSequence:
    nb_element = (
        timecode_end - timecode_begin
    ) // timecode_parameter.position_timecode_rate
    return DanceSequence(
        nb_element
        * [
            json_convertion_constant.from_json_position_to_simulation_position(
                stand_by_position
            )
        ],
        nb_element * [False],
        nb_element * [False],
    )
