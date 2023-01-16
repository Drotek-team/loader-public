import struct
from dataclasses import dataclass
from typing import Any, List, Tuple

from .events import Event, Events
from .events_order import EVENTS_ID, EventsType


@dataclass(frozen=True)
class PositionEvent(Event):
    timecode: int  # time frame associate to the "fps_px4" parameter
    x: int  # x relative coordinate in NED and centimeter between -32 561 and 32 561
    y: int  # y relative coordinate in NED and centimeter between -32 561 and 32 561
    z: int  # z relative coordinate in NED and centimeter between -32 561 and 32 561

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

    def __init__(self):
        self.id_ = EVENTS_ID[EventsType.position]
        self.events: List[PositionEvent] = []

    def __iter__(self):
        yield from self.events

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

    @property
    def generic_events(self) -> List[Event]:
        return self.events  # type: ignore[I an pretty this is a bug from pylance, the typing works if the function return Position with a Event typing]
