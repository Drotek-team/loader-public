import struct
from typing import Any, List, Tuple

from pydantic import BaseModel, StrictInt

from .events import Event, Events


class PositionEvent(BaseModel, Event):
    timecode: StrictInt  # time frame associate to the "fps_px4" parameter
    x: StrictInt  # x relative coordinate in NED and centimeter between -32 561 and 32 561
    y: StrictInt  # y relative coordinate in NED and centimeter between -32 561 and 32 561
    z: StrictInt  # z relative coordinate in NED and centimeter between -32 561 and 32 561

    class Config:
        allow_mutation = False

    # TODO: put a test on that
    @property
    def xyz(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)

    # TODO: put a test on that
    @property
    def get_data(self) -> List[Any]:
        return [self.timecode, self.x, self.y, self.z]


class PositionEvents(Events):
    format_ = ">Ihhh"
    id_ = 0

    def __init__(self):
        self.events: List[PositionEvent] = []

    def __iter__(self):
        yield from self.events

    @property
    def generic_events(self) -> List[Event]:
        return self.events  # type: ignore[I an pretty this is a bug from pylance, the typing works if the function return ColorEvent with a Event typing]

    def add_timecode_xyz(self, timecode: int, xyz: Tuple[int, int, int]) -> None:
        self.events.append(
            PositionEvent(timecode=timecode, x=xyz[0], y=xyz[1], z=xyz[2])
        )

    def add_data(self, data: List[Any]) -> None:
        self.events.append(
            PositionEvent(timecode=data[0], x=data[1], y=data[2], z=data[3])
        )

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
