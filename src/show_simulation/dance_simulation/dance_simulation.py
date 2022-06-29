from dataclasses import dataclass
from typing import List, Tuple

import numpy as np


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
