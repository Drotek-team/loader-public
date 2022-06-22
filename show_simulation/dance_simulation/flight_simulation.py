from typing import Dict, List

import numpy as np

from ...parameter.export_setup import ExportSetup
from .position_simulation import PositionSimulation


def flight_simulation(
    position_events: Dict[int, np.ndarray], export_setup: ExportSetup
) -> np.ndarray:
    position_simulation = PositionSimulation()
    previous_timecode = 0
    flight_positions: List[np.ndarray] = []
    for timecode in position_events:
        if timecode != previous_timecode:
            flight_positions += [
                position_simulation.linear_interpolation(
                    position_events[previous_timecode],
                    position_events[timecode],
                    ratio,
                )
                for ratio in ((timecode - previous_timecode))
                // export_setup.POSITION_TIMECODE_FREQUENCE
            ]
        else:
            flight_positions += [position_events[timecode]]
        previous_timecode = timecode
    return flight_positions
