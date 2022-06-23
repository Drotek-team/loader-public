from dataclasses import dataclass
from typing import Tuple

from .events import Event, Events


class FireEvent(Event):
    def __init__(self, timecode: int, chanel: int, duration: int):
        Event.__init__(self, timecode)
        self.chanel = chanel
        self.duration = duration

    def get_values(self) -> Tuple[int, int]:
        return (self.chanel, self.duration)


class FireEvents(Events):
    format = ">IBB"
    id = 2

    def add(self, timecode: int, chanel: int, duration: int) -> None:
        self.event_list.append(FireEvent(timecode, chanel, duration))
