from dataclasses import dataclass
from typing import Tuple

from .events import Event, Events


class PositionEvent(Event):
    def __init__(self, timecode: int, x: int, y: int, z: int):
        Event.__init__(self, timecode)
        self.x = x
        self.y = y
        self.z = z

    def get_values(self) -> Tuple[int, int, int]:
        return (self.x, self.y, self.z)


class PositionEvents(Events):
    format = ">Ihhh"
    id: int = 0

    def add(self, timecode: int, xyz: Tuple[int, int, int]) -> None:
        self.event_list.append(PositionEvent(timecode, xyz[0], xyz[1], xyz[2]))
