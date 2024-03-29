from dataclasses import dataclass
from typing import Any, List, Tuple

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, MagicNumber

from .events import Event, Events
from .events_order import EventsType


@dataclass(frozen=True)
class PositionEvent(Event):
    frame: int  # time frame associate to the "fps_px4" parameter
    x: int  # x relative coordinate in NED and centimeter
    y: int  # y relative coordinate in NED and centimeter
    z: int  # z relative coordinate in NED and centimeter

    @property
    def xyz(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)

    def get_data(self, magic_number: MagicNumber) -> List[Any]:
        return [
            (
                JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(self.frame)
                if magic_number == MagicNumber.old
                else self.frame
            ),
            self.x,
            self.y,
            self.z,
        ]


class PositionEvents(Events[PositionEvent]):
    def __init__(self, magic_number: MagicNumber) -> None:
        self.format_ = JSON_BINARY_PARAMETERS.position_event_format(magic_number)
        self.id_ = EventsType.position
        self.magic_number = magic_number
        # Had to pass with the init because python mutable defaults are the source of all evil
        # https://florimond.dev/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
        self._events = []

    def add_timecode_xyz(self, frame: int, xyz: Tuple[int, int, int]) -> None:
        self._events.append(PositionEvent(frame=frame, x=xyz[0], y=xyz[1], z=xyz[2]))

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            PositionEvent(
                frame=(
                    JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(data[0])
                    if self.magic_number == MagicNumber.old
                    else data[0]
                ),
                x=data[1],
                y=data[2],
                z=data[3],
            ),
        )
