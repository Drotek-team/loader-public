import struct
from dataclasses import dataclass
from typing import Any, List, Tuple

from .events import Event, Events


# TODO: passer à pydantic
@dataclass(frozen=True)
class PositionEvent(Event):
    timecode: int  # time frame associate to the "fps_px4" parameter
    x: int  # x relative coordinate in NED and centimeter between -32 561 and 32 561
    y: int  # y relative coordinate in NED and centimeter between -32 561 and 32 561
    z: int  # z relative coordinate in NED and centimeter between -32 561 and 32 561

    def __post_init__(self):
        if not (isinstance(self.timecode, int)):
            msg = f"This value {self.timecode} should be an integer"
            raise ValueError(msg)
        if not (isinstance(self.x, int)):
            msg = f"This value {self.x} should be an integer"
            raise ValueError(msg)
        if not (isinstance(self.y, int)):
            msg = f"This value {self.y} should be an integer"
            raise ValueError(msg)
        if not (isinstance(self.z, int)):
            msg = f"This value {self.z} should be an integer"
            raise ValueError(msg)

    @property
    def xyz(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)

    def get_data(self) -> Tuple[int, int, int, int]:
        return (self.timecode, self.x, self.y, self.z)


# TODO: you know you can do much better for that class typing
class PositionEvents(Events):
    events: List[PositionEvent]
    format_ = ">Ihhh"
    id_ = 0

    def __init__(self):
        self.events = []

    def __iter__(self):
        yield from self.events

    def add_timecode_xyz(self, timecode: int, xyz: Tuple[int, int, int]) -> None:
        self.events.append(PositionEvent(timecode, xyz[0], xyz[1], xyz[2]))

    def add_data(self, data: Tuple[Any, Any, Any, Any]) -> None:
        self.events.append(PositionEvent(data[0], data[1], data[2], data[3]))

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

    def get_xyz_by_event_index(self, event_index: int) -> Tuple[int, int, int]:
        return self.events[event_index].xyz
