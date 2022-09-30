from typing import Tuple

from .events import Event, Events
from typing import List
import struct


class FireEvent(Event):
    def __init__(self, frame: int, chanel: int, duration: int):
        self.frame = frame
        self.chanel = chanel
        self.duration = duration

    @property
    def chanel_duration(self) -> Tuple[int, int]:
        return (self.chanel, self.duration)

    def get_data(self) -> Tuple[int, int, int]:
        return (self.frame, self.chanel, self.duration)


class FireEvents(Events):
    events: List[FireEvent]
    format = ">HBB"
    id = 2

    def __init__(self):
        self.events = []

    def add_frame_rgbw(self, frame: int, chanel: int, duration: int) -> None:
        self.events.append(FireEvent(frame, chanel, duration))

    def add_data(self, data: Tuple) -> None:
        self.events.append(FireEvent(data[0], data[1], data[2]))

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
