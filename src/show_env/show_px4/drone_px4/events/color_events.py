from dataclasses import dataclass
from typing import Any, List, Tuple

from .events import Event, Events
from .events_order import EVENTS_ID, EventsType


@dataclass(frozen=True)
class ColorEvent(Event):
    timecode: int  # time frame associate to the "fps_px4" parameter
    r: int  # red color between 0 and 255
    g: int  # green color between 0 and 255
    b: int  # blue color between 0 and 255
    w: int  # white color between 0 and 255

    @property
    def rgbw(self) -> Tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.w)

    @property
    def get_data(self) -> List[Any]:
        return [self.timecode, self.r, self.g, self.b, self.w]


class ColorEvents(Events):
    format_ = ">IBBBB"
    id_ = EVENTS_ID[EventsType.color]

    def __init__(self):
        # Had to pass with the init because python mutable defaults are the source of all evil
        # https://florimond.dev/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
        self._events: List[Event] = []

    def add_timecode_rgbw(self, timecode: int, rgbw: Tuple[int, int, int, int]) -> None:
        self._events.append(
            ColorEvent(timecode=timecode, r=rgbw[0], g=rgbw[1], b=rgbw[2], w=rgbw[3])
        )

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            ColorEvent(timecode=data[0], r=data[1], g=data[2], b=data[3], w=data[4])
        )

    def get_color_event_by_index(self, index: int) -> ColorEvent:
        color_event_data = self._events[index].get_data
        return ColorEvent(
            timecode=color_event_data[0],
            r=color_event_data[1],
            g=color_event_data[2],
            b=color_event_data[3],
            w=color_event_data[4],
        )

    @property
    def specific_events(self) -> List[ColorEvent]:
        return [
            self.get_color_event_by_index(event_index)
            for event_index in range(len(self._events))
        ]
