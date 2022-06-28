from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


@dataclass(frozen=True)
class DroneSimulationConvertor:
    CENTIMETER_TO_METER_RATIO: float = 1e-2
    TIMECODE_TO_SECOND_RATIO: float = 1e-3

    def event_xyz_to_numpy_position(
        self, xyz: Tuple[float, float, float]
    ) -> np.ndarray:
        return np.array(
            (
                self.CENTIMETER_TO_METER_RATIO * xyz[1],
                self.CENTIMETER_TO_METER_RATIO * xyz[0],
                -self.CENTIMETER_TO_METER_RATIO * xyz[2],
            )
        )


@dataclass
class DanceSequence:
    drone_positions: List[np.ndarray]
    drone_in_air: List[bool]
    drone_in_dance: List[bool]


class DanceSimulation:
    def __init__(self):
        self.dance_sequence = DanceSequence([], [], [])

    def update(self, dance_sequence: DanceSequence) -> None:
        self.dance_sequence.drone_positions += dance_sequence.drone_positions
        self.dance_sequence.drone_in_air += dance_sequence.drone_in_air
        self.dance_sequence.drone_in_dance += dance_sequence.drone_in_dance
