from dataclasses import dataclass
from typing import Tuple


@dataclass
class EventsSizeEasing:
    previous_xyz: Tuple[int, int, int] = (0, 0, 0)
    previous_rgbw: Tuple[int, int, int, int] = (0, 0, 0, 0)

    def reset_previous_events(self) -> None:
        self.previous_position = (0, 0, 0)
        self.previous_rgbw = (0, 0, 0, 0)

    def is_xyz_valid(self, xyz: Tuple[int, int, int]) -> bool:
        valid_event = xyz != self.previous_xyz
        self.previous_xyz = xyz
        return valid_event

    def is_rgbw_valid(self, rgbw: Tuple[int, int, int, int]) -> bool:
        valid_event = rgbw != self.previous_rgbw
        self.previous_rgbw = rgbw
        return valid_event


# TODO: apply_dance_size_relief