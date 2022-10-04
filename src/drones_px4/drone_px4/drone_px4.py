from dataclasses import dataclass
from typing import List, Tuple

from .events.color_events import ColorEvents
from .events.events import Events
from .events.fire_events import FireEvents
from .events.position_events import PositionEvent, PositionEvents


class DronePx4:
    def __init__(self, index: int):
        self.index = index
        self.position_events = PositionEvents()
        self.color_events = ColorEvents()
        self.fire_events = FireEvents()

    def add_position(self, frame: int, xyz: Tuple[int, int, int]) -> None:
        self.position_events.add_frame_xyz(frame, xyz)

    def add_color(self, frame: int, rgbw: Tuple[int, int, int, int]) -> None:
        self.color_events.add_frame_rgbw(frame, rgbw)

    def add_fire(self, frame: int, chanel: int, duration_frame: int) -> None:
        self.fire_events.add_frame_chanel_duration(frame, chanel, duration_frame)

    ### TO DO: not very clean but doing an enum class of the events just for this is kind of overkill
    def get_events_by_index(self, event_index: int) -> Events:
        events_enum = {
            self.position_events.id: self.position_events,
            self.color_events.id: self.color_events,
            self.fire_events.id: self.fire_events,
        }
        if not (event_index in events_enum.keys()):
            raise ValueError(event_index)
        return events_enum[event_index]

    @property
    def last_position_event(self) -> PositionEvent:
        return self.position_events.events[-1]

    @property
    def first_xyz(self) -> Tuple:
        return self.position_events.get_xyz_by_event_index(0)

    @property
    def last_xyz(self) -> Tuple:
        if self.position_events.events == []:
            return (0, 0, 0)
        return self.position_events.get_xyz_by_event_index(-1)

    @property
    def last_rgbw(self) -> Tuple:
        if self.color_events.events == []:
            return (0, 0, 0, 0)
        return self.color_events.get_rgbw_by_event_index(-1)

    @property
    def events_list(self) -> List[Events]:
        return [self.position_events, self.color_events, self.fire_events]

    @property
    def non_empty_events_list(self) -> List[Events]:
        return [event for event in self.events_list if event.event_size]
