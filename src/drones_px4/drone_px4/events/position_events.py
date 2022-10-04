from dataclasses import dataclass
from typing import Tuple, List

from .events import Event, Events
import struct


@dataclass(frozen=True)
class PositionEvent(Event):
    frame: int  # time frame associate to the "fps_px4" parameter
    x: int  # x relative coordinate in centimeter between 0 and 32561
    y: int  # y relative coordinate in centimeter between 0 and 32561
    z: int  # z relative coordinate in centimeter between 0 and 32561

    @property
    def xyz(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)

    def get_data(self) -> Tuple[int, int, int, int]:
        return (self.frame, self.x, self.y, self.z)


class PositionEvents(Events):
    events: List[PositionEvent]
    format = ">Hhhh"
    id = 0

    def __init__(self):
        self.events = []

    def add_frame_xyz(self, frame: int, xyz: Tuple[int, int, int]) -> None:
        self.events.append(PositionEvent(frame, xyz[0], xyz[1], xyz[2]))

    def add_data(self, data: Tuple) -> None:
        self.events.append(PositionEvent(data[0], data[1], data[2], data[3]))

    @property
    def event_size(self):
        return struct.calcsize(self.format)

    @property
    def events_size(self):
        return len(self.events) * struct.calcsize(self.format)

    @property
    def nb_events(self) -> int:
        return len(self.events)

    def get_frame_by_event_index(self, event_index: int) -> int:
        return self.events[event_index].frame

    def get_xyz_by_event_index(self, event_index: int) -> Tuple[int, int, int]:
        return self.events[event_index].xyz
