import struct
from dataclasses import dataclass
from typing import List, Tuple

from .events import Event, Events


@dataclass(frozen=True)
class FireEvent(Event):
    frame: int  # time frame associate to the "fps_px4" parameter
    chanel: int  # chanel of the fire event
    duration: int  # duration of the fire event in timecode

    def __post_init__(self):
        if not (isinstance(self.frame, int)):
            msg = "This value should be an integer"
            raise ValueError(msg)
        if not (isinstance(self.chanel, int)):
            msg = "This value should be an integer"
            raise ValueError(msg)
        if not (isinstance(self.duration, int)):
            msg = "This value should be an integer"
            raise ValueError(msg)

    @property
    def chanel_duration(self) -> Tuple[int, int]:
        return (self.chanel, self.duration)

    def get_data(self) -> Tuple[int, int, int]:
        return (self.frame, self.chanel, self.duration)


class FireEvents(Events):
    events: List[FireEvent]
    format_ = ">HBB"
    id_ = 2

    def __init__(self):
        self.events = []

    def add_frame_chanel_duration(self, frame: int, chanel: int, duration: int) -> None:
        self.events.append(FireEvent(frame, chanel, duration))

    def add_data(self, data: Tuple) -> None:
        self.events.append(FireEvent(data[0], data[1], data[2]))

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
        return self.events[event_index].frame
