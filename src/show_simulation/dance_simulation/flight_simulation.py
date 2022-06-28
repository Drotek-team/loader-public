from typing import Dict, List

import numpy as np

from ...parameter.parameter import TimecodeParameter
from .dance_simulation import DanceSequence
from .position_simulation import linear_interpolation


def flight_simulation(
    position_events: Dict[int, np.ndarray], timecode_parameter: TimecodeParameter
) -> DanceSequence:
    previous_timecode = 0
    flight_positions: List[np.ndarray] = []
    for timecode in position_events:
        if timecode != previous_timecode:
            flight_positions += [
                linear_interpolation(
                    position_events[previous_timecode],
                    position_events[timecode],
                    ratio,
                )
                for ratio in ((timecode - previous_timecode))
                // timecode_parameter.position_timecode_rate
            ]
        else:
            flight_positions += [position_events[timecode]]
        previous_timecode = timecode
    return DanceSequence(
        flight_positions, len(flight_positions) * [True], len(flight_positions) * [True]
    )
