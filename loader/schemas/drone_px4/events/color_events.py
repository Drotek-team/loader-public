from dataclasses import dataclass
from typing import Any, List, Tuple

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, MagicNumber

from .events import Event, Events
from .events_order import EventsType


@dataclass(frozen=True)
class ColorEvent(Event):
    frame: int  # time frame associate to the "fps_px4" parameter
    r: int  # red color
    g: int  # green color
    b: int  # blue color
    w: int  # white color

    @property
    def rgbw(self) -> Tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.w)

    def get_data(self, magic_number: MagicNumber) -> List[Any]:
        return [
            (
                JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(self.frame)
                if magic_number == MagicNumber.old
                else self.frame
            ),
            self.r,
            self.g,
            self.b,
            self.w,
        ]


class ColorEvents(Events[ColorEvent]):
    def __init__(self, magic_number: MagicNumber) -> None:
        self.id_ = EventsType.color
        self.format_ = JSON_BINARY_PARAMETERS.color_event_format(magic_number)
        self.magic_number = magic_number
        # Had to pass with the init because python mutable defaults are the source of all evil
        # https://florimond.dev/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
        self._events = []

    def add_timecode_rgbw(self, frame: int, rgbw: Tuple[int, int, int, int]) -> None:
        self._events.append(ColorEvent(frame=frame, r=rgbw[0], g=rgbw[1], b=rgbw[2], w=rgbw[3]))

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            ColorEvent(
                frame=(
                    JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(data[0])
                    if self.magic_number == MagicNumber.old
                    else data[0]
                ),
                r=data[1],
                g=data[2],
                b=data[3],
                w=data[4],
            ),
        )
