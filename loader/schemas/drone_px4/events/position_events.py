from dataclasses import dataclass
from typing import Any, List, Tuple

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS

from .events import Event, Events
from .events_order import EventsType


@dataclass(frozen=True)
class PositionEvent(Event):
    timecode: int  # time frame associate to the "fps_px4" parameter
    x: int  # x relative coordinate in NED and centimeter
    y: int  # y relative coordinate in NED and centimeter
    z: int  # z relative coordinate in NED and centimeter

    @property
    def xyz(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)

    @property
    def get_data(self) -> List[Any]:
        return [self.timecode, self.x, self.y, self.z]


class PositionEvents(Events[PositionEvent]):
    def __init__(self) -> None:
        self.format_ = JSON_BINARY_PARAMETERS.position_event_format
        self.id_ = EventsType.position
        # Had to pass with the init because python mutable defaults are the source of all evil
        # https://florimond.dev/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
        self._events = []

    def add_timecode_xyz(self, frame: int, xyz: Tuple[int, int, int]) -> None:
        self._events.append(
            PositionEvent(
                timecode=JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(frame),
                x=xyz[0],
                y=xyz[1],
                z=xyz[2],
            ),
        )

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            PositionEvent(timecode=data[0], x=data[1], y=data[2], z=data[3]),
        )
