from typing import List, Tuple

from .convex_hull import calculate_convex_hull
from .drone_px4.drone_px4 import DronePx4
from .drone_px4.events_size_easing import EventsSizeEasing, apply_dance_size_relief


class ShowPx4(List[DronePx4]):
    @property
    def nb_drone(self) -> int:
        return len(self)

    @property
    def duration(self) -> int:
        return max(drone.last_position_event.timecode for drone in self)

    @property
    def first_horizontal_positions(self) -> List[Tuple[int, int]]:
        return [(drone.first_xyz[0], drone.first_xyz[1]) for drone in self]

    @property
    def convex_hull(self) -> List[Tuple[int, int]]:
        return calculate_convex_hull(self.first_horizontal_positions)

    @property
    def altitude_range(self) -> Tuple[float, float]:
        z_positions = [
            position_event.xyz[2]
            for drone in self
            for position_event in drone.position_events.events
        ]
        return (min(z_positions), max(z_positions))

    def apply_dances_size_relief(self) -> None:
        events_size_easing = EventsSizeEasing()
        for drone in self:
            apply_dance_size_relief(drone, events_size_easing)
