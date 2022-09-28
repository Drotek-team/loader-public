from dataclasses import dataclass
from typing import Tuple

from .events import Event, Events


class FireEvent(Event):
    def __init__(self, frame: int, chanel: int, duration_frame: int):
        Event.__init__(self, frame)
        self.chanel = chanel
        self.duration_frame = duration_frame

    def get_values(self) -> Tuple[int, int]:
        return (self.chanel, self.duration_frame)

    def get_raw_data(self) -> Tuple[int, int, int]:
        return (self.frame, self.chanel, self.duration_frame)


class FireEvents(Events):
    format = ">HBB"
    id = 2

    def add(self, frame: int, chanel: int, duration_frame: int) -> None:
        self.event_list.append(FireEvent(frame, chanel, duration_frame))

    def add_raw_data(self, data: Tuple[int, int, int]) -> None:
        self.event_list.append(FireEvent(data[0], data[1], data[2]))
