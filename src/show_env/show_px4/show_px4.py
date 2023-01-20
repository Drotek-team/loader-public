from typing import List

from .drone_px4.drone_px4 import DronePx4
from .drone_px4.events_size_easing import EventsSizeEasing, apply_dance_size_relief


class ShowPx4(List[DronePx4]):
    @property
    def nb_drone(self) -> int:
        return len(self)

    @property
    def duration(self) -> int:
        return max(drone_px4.position_events[-1].timecode for drone_px4 in self)

    def apply_dances_size_relief(self) -> None:
        events_size_easing = EventsSizeEasing()
        for drone in self:
            apply_dance_size_relief(drone, events_size_easing)
        events_size_easing = EventsSizeEasing()
        for drone in self:
            apply_dance_size_relief(drone, events_size_easing)
