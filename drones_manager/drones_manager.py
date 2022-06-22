from typing import List, Tuple

import numpy as np

from .convex_hull import calculate_convex_hull
from .drone.drone import Drone
from .drone.events_size_easing import apply_dance_size_relief


class DronesManager:
    def __init__(self, drones: List[Drone]):
        self.drones = drones

    @property
    def first_horizontal_positions(self) -> List[Tuple]:
        return [
            drone.position_events.get_values_by_event_index(0) for drone in self.drones
        ]

    @property
    def convex_hull(self) -> List[np.ndarray]:
        return calculate_convex_hull(np.array(self.first_horizontal_positions))

    def apply_dances_size_relief(self) -> None:
        for drone in self.drones:
            apply_dance_size_relief(drone)

    def get_end_show_timecode(self) -> int:
        return max(
            drone.position_events.get_timecode_by_event_index(-1)
            for drone in self.drones
        )
