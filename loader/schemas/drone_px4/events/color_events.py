from dataclasses import dataclass
from typing import Any, List, Tuple

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS

from .events import Event, Events
from .events_order import EventsType


@dataclass(frozen=True)
class ColorEvent(Event):
    timecode: int  # time frame associate to the "fps_px4" parameter
    r: int  # red color
    g: int  # green color
    b: int  # blue color
    w: int  # white color

    @property
    def rgbw(self) -> Tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.w)

    @property
    def get_data(self) -> List[Any]:
        return [self.timecode, self.r, self.g, self.b, self.w]


class ColorEvents(Events[ColorEvent]):
    def __init__(self) -> None:
        self.id_ = EventsType.color
        self.format_ = JSON_BINARY_PARAMETERS.color_event_format
        # Had to pass with the init because python mutable defaults are the source of all evil
        # https://florimond.dev/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
        self._events = []

    def add_timecode_rgbw(self, frame: int, rgbw: Tuple[int, int, int, int]) -> None:
        self._events.append(
            ColorEvent(
                timecode=JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(frame),
                r=rgbw[0],
                g=rgbw[1],
                b=rgbw[2],
                w=rgbw[3],
            ),
        )

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            ColorEvent(timecode=data[0], r=data[1], g=data[2], b=data[3], w=data[4]),
        )
