from typing import List

from .drone_px4.drone_px4 import DronePx4


class ShowPx4(List[DronePx4]):
    @property
    def nb_drone(self) -> int:
        return len(self)

    @property
    def duration(self) -> int:
        return max(drone_px4.position_events[-1].timecode for drone_px4 in self)

    def apply_dances_size_relief(self) -> None:
        pass
