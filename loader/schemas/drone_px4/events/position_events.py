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
    scale: int  # position scale

    @property
    def xyz(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)

    def get_data(self, magic_number: MagicNumber) -> List[Any]:
        return [
            (
                JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(self.frame)
                if magic_number == MagicNumber.v1
                else self.frame
            ),
            round(self.x / self.scale),
            round(self.y / self.scale),
            round(self.z / self.scale),
        ]

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return (
                self.frame == other.frame
                and self.scale == other.scale
                and abs(self.x - other.x) < self.scale
                and abs(self.y - other.y) < self.scale
                and abs(self.z - other.z) < self.scale
            )
        return False  # pragma: no cover


class PositionEvents(Events[PositionEvent]):
    def __init__(self, magic_number: MagicNumber, scale: int) -> None:
        self.format_ = JSON_BINARY_PARAMETERS.position_event_format(magic_number)
        self.id_ = EventsType.position
        self.magic_number = magic_number
        self.scale = scale
        # Had to pass with the init because python mutable defaults are the source of all evil
        # https://florimond.dev/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
        self._events = []

    def add_timecode_xyz(self, frame: int, xyz: Tuple[int, int, int]) -> None:
        self._events.append(
            PositionEvent(frame=frame, x=xyz[0], y=xyz[1], z=xyz[2], scale=self.scale)
        )

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            PositionEvent(
                frame=(
                    JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(data[0])
                    if self.magic_number == MagicNumber.v1
                    else data[0]
                ),
                x=data[1] * self.scale,
                y=data[2] * self.scale,
                z=data[3] * self.scale,
                scale=self.scale,
            ),
        )
