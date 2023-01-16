from dataclasses import dataclass
from typing import List, Tuple

from .drone_px4 import DronePx4


@dataclass
class EventsSizeEasing:
    previous_xyz: Tuple[int, int, int] = (0, 0, 0)
    previous_rgbw: Tuple[int, int, int, int] = (0, 0, 0, 0)

    def reset_previous_events(self):
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


def apply_dance_size_relief(drone: DronePx4, events_size_easing: EventsSizeEasing):
    events_size_easing.reset_previous_events()
    valid_position_indices: List[int] = []
    for position_event_index, position_event in enumerate(drone.position_events):
        if events_size_easing.is_xyz_valid(position_event.xyz):
            valid_position_indices.append(position_event_index)

    valid_color_indices: List[int] = []
    for color_event_index, color_event in enumerate(drone.color_events):
        if events_size_easing.is_rgbw_valid(color_event.rgbw):
            valid_color_indices.append(color_event_index)
