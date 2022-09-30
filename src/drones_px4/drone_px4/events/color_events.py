from typing import Tuple

from .events import Event, Events
from typing import List
import struct


class ColorEvent(Event):
    def __init__(self, frame: int, r: int, g: int, b: int, w: int):
        self.frame = frame
        self.r = r
        self.g = g
        self.b = b
        self.w = w

    @property
    def rgbw(self) -> Tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.w)

    def get_data(self) -> Tuple[int, int, int, int, int]:
        return (self.frame, self.r, self.g, self.b, self.w)


class ColorEvents(Events):
    events: List[ColorEvent]
    format = ">HBBBB"
    id: int = 1

    def __init__(self):
        self.events = []

    def add_frame_rgbw(self, frame: int, rgbw: Tuple[int, int, int, int]) -> None:
        self.events.append(ColorEvent(frame, rgbw[0], rgbw[1], rgbw[2], rgbw[3]))

    def add_data(self, data: Tuple) -> None:
        self.events.append(ColorEvent(data[0], data[1], data[2], data[3], data[4]))

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

    def get_rgbw_by_event_index(self, event_index: int) -> Tuple:
        return self.events[event_index].rgbw
