import struct
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

    def __init__(self):
        self.id_ = EVENTS_ID[EventsType.color]
        self._events: List[ColorEvent] = []

    def __iter__(self):
        yield from self._events

    def __getitem__(self, color_event_index: int):
        return self._events[color_event_index]

    def __len__(self) -> int:
        return len(self._events)

    @property
    def generic_events(self) -> List[Event]:
        return self._events  # type: ignore[I an pretty this is a bug from pylance, the typing works if the function return ColorEvent with a Event typing]

    def add_timecode_rgbw(self, timecode: int, rgbw: Tuple[int, int, int, int]) -> None:
        self._events.append(
            ColorEvent(timecode=timecode, r=rgbw[0], g=rgbw[1], b=rgbw[2], w=rgbw[3])
        )

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            ColorEvent(timecode=data[0], r=data[1], g=data[2], b=data[3], w=data[4])
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
