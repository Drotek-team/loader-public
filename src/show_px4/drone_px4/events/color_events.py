import struct
from dataclasses import dataclass
from typing import List, Tuple

from .events import Event, Events


@dataclass(frozen=True)
class ColorEvent(Event):
    timecode: int  # time frame associate to the "fps_px4" parameter
    r: int  # red color between 0 and 255
    g: int  # green color between 0 and 255
    b: int  # blue color between 0 and 255
    w: int  # white color between 0 and 255

    def __post_init__(self):
        if not (isinstance(self.timecode, int)):
            msg = "This value should be an integer"
            raise ValueError(msg)
        if not (isinstance(self.r, int)):
            msg = "This value should be an integer"
            raise ValueError(msg)
        if not (isinstance(self.g, int)):
            msg = "This value should be an integer"
            raise ValueError(msg)
        if not (isinstance(self.b, int)):
            msg = "This value should be an integer"
            raise ValueError(msg)
        if not (isinstance(self.w, int)):
            msg = "This value should be an integer"
            raise ValueError(msg)

    @property
    def rgbw(self) -> Tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.w)

    def get_data(self) -> Tuple[int, int, int, int, int]:
        return (self.timecode, self.r, self.g, self.b, self.w)


class ColorEvents(Events):
    events: List[ColorEvent]
    format_ = ">HBBBB"
    id_: int = 1

    def __init__(self):
        self.events = []

    def add_timecode_rgbw(self, timecode: int, rgbw: Tuple[int, int, int, int]) -> None:
        self.events.append(ColorEvent(timecode, rgbw[0], rgbw[1], rgbw[2], rgbw[3]))

    def add_data(self, data: Tuple) -> None:
        self.events.append(ColorEvent(data[0], data[1], data[2], data[3], data[4]))

    @property
    def event_size(self):
        return struct.calcsize(self.format_)

    @property
    def events_size(self):
        return len(self.events) * struct.calcsize(self.format_)

    @property
    def nb_events(self) -> int:
        return len(self.events)

    def get_frame_by_event_index(self, event_index: int) -> int:
        return self.events[event_index].timecode

    def get_rgbw_by_event_index(self, event_index: int) -> Tuple[int, int, int, int]:
        return self.events[event_index].rgbw
