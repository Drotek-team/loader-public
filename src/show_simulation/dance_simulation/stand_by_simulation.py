from typing import Tuple

from ...parameter.parameter import JsonConventionConstant, TimecodeParameter
from .dance_simulation import DanceSequence


def stand_by_simulation(
    timecode_begin: int,
    timecode_end: int,
    stand_by_position: Tuple[int, int, int],
    timecode_parameter: TimecodeParameter,
    json_convention_constant: JsonConventionConstant,
) -> DanceSequence:
    nb_element = (
        timecode_end - timecode_begin
    ) // timecode_parameter.position_timecode_rate
    return DanceSequence(
        nb_element
        * [
            json_convention_constant.from_json_position_to_simulation_position(
                stand_by_position
            )
        ],
        nb_element * [False],
        nb_element * [False],
    )
