from typing import List, Tuple

from .events.color_events import ColorEvents
from .events.events import Events
from .events.fire_events import FireEvents
from .events.position_events import PositionEvents


# Improve: en reparler pour généraliser nouveau drone
class DronePx4:
    def __init__(self, index: int) -> None:
        self.index = index
        self.position_events = PositionEvents()
        self.color_events = ColorEvents()
        self.fire_events = FireEvents()

    def __eq__(self, other_drone_px4: object) -> bool:
        if isinstance(other_drone_px4, DronePx4):
            return (
                self.index == self.index
                and self.position_events == other_drone_px4.position_events
                and self.color_events == other_drone_px4.color_events
                and self.fire_events == other_drone_px4.fire_events
            )
        return False

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
            msg = f"{event_index} is not inside the events enum {events_enum.keys()}"
            raise IndexError(msg)
        return events_enum[event_index]

    @property
    def events_list(self) -> List[Events]:
        return [self.position_events, self.color_events, self.fire_events]

    @property
    def non_empty_events_list(self) -> List[Events]:
        return [events for events in self.events_list if events]
        return [events for events in self.events_list if events]
