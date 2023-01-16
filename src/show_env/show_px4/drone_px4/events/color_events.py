import struct
from typing import Any, List, Tuple

from pydantic import BaseModel, StrictInt

from .events import Event, Events


class ColorEvent(Event, BaseModel):
    timecode: StrictInt  # time frame associate to the "fps_px4" parameter
    r: StrictInt  # red color between 0 and 255
    g: StrictInt  # green color between 0 and 255
    b: StrictInt  # blue color between 0 and 255
    w: StrictInt  # white color between 0 and 255

    class Config:
        allow_mutation = False

    # TODO: put a test on that
    @property
    def rgbw(self) -> Tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.w)

    # TODO: put a test on that
    @property
    def get_data(self) -> List[Any]:
        return [self.timecode, self.r, self.g, self.b, self.w]


class ColorEvents(Events):
    format_ = ">IBBBB"
    id_: int = 1

    def __init__(self):
        self.events: List[ColorEvent] = []

    @property
    def generic_events(self) -> List[Event]:
        return self.events  # type: ignore[I an pretty this is a bug from pylance, the typing works if the function return ColorEvent with a Event typing]

    def add_timecode_rgbw(self, timecode: int, rgbw: Tuple[int, int, int, int]) -> None:
        self.events.append(
            ColorEvent(timecode=timecode, r=rgbw[0], g=rgbw[1], b=rgbw[2], w=rgbw[3])
        )

    def add_data(self, data: List[Any]) -> None:
        self.events.append(
            ColorEvent(timecode=data[0], r=data[1], g=data[2], b=data[3], w=data[4])
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

    def get_frame_by_event_index(self, event_index: int) -> int:
        return self.events[event_index].timecode

    def get_rgbw_by_event_index(self, event_index: int) -> Tuple[int, int, int, int]:
        return self.events[event_index].rgbw
