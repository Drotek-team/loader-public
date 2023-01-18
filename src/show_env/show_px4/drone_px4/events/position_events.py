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
    def __init__(self):
        self.format_ = ">Ihhh"
        self.id_ = EVENTS_ID[EventsType.position]
        # Had to pass with the init because python mutable defaults are the source of all evil
        # https://florimond.dev/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
        self._events = []

    def add_timecode_xyz(self, timecode: int, xyz: Tuple[int, int, int]) -> None:
        self._events.append(
            PositionEvent(timecode=timecode, x=xyz[0], y=xyz[1], z=xyz[2])
        )

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            PositionEvent(timecode=data[0], x=data[1], y=data[2], z=data[3])
        )

    def get_position_event_by_index(self, index: int) -> PositionEvent:
        position_event_data = self._events[index].get_data
        return PositionEvent(
            timecode=position_event_data[0],
            x=position_event_data[1],
            y=position_event_data[2],
            z=position_event_data[3],
        )

    @property
    def specific_events(self) -> List[PositionEvent]:
        return [
            self.get_position_event_by_index(event_index)
            for event_index in range(len(self._events))
        ]
