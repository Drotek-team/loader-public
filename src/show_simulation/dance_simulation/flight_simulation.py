from typing import Dict, List, Tuple

import numpy as np

from ...drones_manager.drone.events.position_events import PositionEvent
from ...parameter.parameter import JsonConvertionConstant, TimecodeParameter
from .dance_simulation import DanceSequence
from .position_simulation import linear_interpolation


def flight_simulation(
    position_events: List[PositionEvent],
    timecode_parameter: TimecodeParameter,
    json_convertion_constant: JsonConvertionConstant,
) -> DanceSequence:
    flight_positions: List[np.ndarray] = []
    for position_event, next_position_event in zip(
        position_events[:-1], position_events[1:]
    ):
        flight_positions += linear_interpolation(
            position_event.get_values(),
            next_position_event.get_values(),
            ((next_position_event.timecode - position_event.timecode))
            // timecode_parameter.position_timecode_rate,
            json_convertion_constant,
        )
    # flight_positions.append(
    #     json_convertion_constant.from_json_position_to_simulation_position(
    #         position_events[-1].get_values()
    #     )
    # )
    return DanceSequence(
        flight_positions, len(flight_positions) * [True], len(flight_positions) * [True]
    )
