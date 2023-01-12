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

    def add_position(self, timecode: int, xyz: Tuple[int, int, int]) -> None:
        self.position_events.add_timecode_xyz(timecode, xyz)

    def add_color(self, timecode: int, rgbw: Tuple[int, int, int, int]) -> None:
        self.color_events.add_timecode_rgbw(timecode, rgbw)

    def add_fire(self, timecode: int, chanel: int, duration_frame: int) -> None:
        self.fire_events.add_timecode_chanel_duration(timecode, chanel, duration_frame)

    def get_events_by_index(self, event_index: int) -> Events:
        events_enum = {
            self.position_events.id_: self.position_events,
            self.color_events.id_: self.color_events,
            self.fire_events.id_: self.fire_events,
        }
        if event_index not in events_enum.keys():
            raise ValueError(event_index)
        return events_enum[event_index]

    @property
    def last_position_event(self) -> PositionEvent:
        return self.position_events.events[-1]

    @property
    def first_xyz(self) -> Tuple[int, int, int]:
        return self.position_events.get_xyz_by_event_index(0)

    @property
    def last_xyz(self) -> Tuple[int, int, int]:
        if self.position_events.events == []:
            return (0, 0, 0)
        return self.position_events.get_xyz_by_event_index(-1)

    @property
    def last_rgbw(self) -> Tuple[int, int, int, int]:
        if self.color_events.events == []:
            return (0, 0, 0, 0)
        return self.color_events.get_rgbw_by_event_index(-1)

    # TODO place a test on that
    @property
    def events_list(self) -> List[Events]:
        return [self.position_events, self.color_events, self.fire_events]

    # TODO place a test on that
    @property
    def non_empty_events_list(self) -> List[Events]:
        return [events for events in self.events_list if events.events]
