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

    @property
    def xyz(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)

    @property
    def get_data(self) -> List[Any]:
        return [self.timecode, self.x, self.y, self.z]


class PositionEvents(Events):
    format_ = ">Ihhh"

    def __init__(self):
        self.id_ = EVENTS_ID[EventsType.position]
        # TODO: !!!!!!!!!!!!! make this one an event !!!!!!!!!!!!!!!!!!
        self._events: List[PositionEvent] = []

    def __iter__(self):
        yield from self._events

    def __getitem__(self, position_event_index: int):
        return self._events[position_event_index]

    def __len__(self) -> int:
        return len(self._events)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, PositionEvents) and len(self) == len(other):
            return all(
                [
                    self._events[event_index] == other._events[event_index]
                    for event_index in range(len(self._events))
                ]
            )
        return False

    def add_timecode_xyz(self, timecode: int, xyz: Tuple[int, int, int]) -> None:
        self._events.append(
            PositionEvent(timecode=timecode, x=xyz[0], y=xyz[1], z=xyz[2])
        )

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            PositionEvent(timecode=data[0], x=data[1], y=data[2], z=data[3])
        )

    @property
    def event_size(self):
        return struct.calcsize(self.format_)

    @property
    def events_size(self):
        return len(self._events) * struct.calcsize(self.format_)

    @property
    def nb_events(self) -> int:
        return len(self._events)

    @property
    def generic_events(self) -> List[Event]:
        return self._events  # type: ignore[I an pretty this is a bug from pylance, the typing works if the function return Position with a Event typing]
