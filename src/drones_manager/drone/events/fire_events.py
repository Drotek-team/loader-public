from dataclasses import dataclass
from typing import Tuple

from .events import Event, Events


@dataclass(frozen=True)
class FireEvent(Event):
    def __init__(self, timecode: int, chanel: int, value: int):
        Event.__init__(self, timecode)
        self.chanel = chanel
        self.value = value

    def get_values(self) -> Tuple[int, int]:
        return (self.chanel, self.value)


class FireEvents(Events):
    format = ">IBB"
    id = 2

    def add(self, timecode: int, chanel: int, value: int) -> None:
        self.event_list.append(FireEvent(timecode, chanel, value))
