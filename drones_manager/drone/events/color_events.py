from dataclasses import dataclass
from typing import Tuple

from .events import Event, Events


@dataclass(frozen=True)
class ColorEvent(Event):
    def __init__(self, timecode: int, r: int, g: int, b: int, w: int):
        Event.__init__(self, timecode)
        self.r = r
        self.g = g
        self.b = b
        self.w = w

    def get_values(self) -> Tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.w)


class ColorEvents(Events):
    format = ">IBBBB"
    id: int = 1

    def add(self, timecode: int, rgbw: Tuple[int, int, int, int]) -> None:
        self.event_list.append(ColorEvent(timecode, rgbw[0], rgbw[1], rgbw[2], rgbw[3]))
