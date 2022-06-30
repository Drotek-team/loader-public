from typing import List, Tuple

from .events.color_events import ColorEvents
from .events.events import Events
from .events.fire_events import FireEvents
from .events.position_events import PositionEvent, PositionEvents


class Drone:
    def __init__(self):
        self.position_events = PositionEvents()
        self.color_events = ColorEvents()
        self.fire_events = FireEvents()

    def add_position(self, timecode: int, xyz: Tuple[int, int, int]) -> None:
        self.position_events.add(timecode, xyz)

    def add_color(self, timecode: int, rgbw: Tuple[int, int, int, int]) -> None:
        self.color_events.add(timecode, rgbw)

    def add_fire(self, timecode: int, value: float) -> None:
        self.fire_events.add(timecode, value)

    @property
    def last_position_event(self) -> List[PositionEvent]:
        return self.position_events[-1]

    @property
    def first_xyz(self) -> Tuple:
        return self.position_events.get_values_by_event_index(0)

    @property
    def events_list(self) -> List[Events]:
        return [self.position_events, self.color_events, self.fire_events]
