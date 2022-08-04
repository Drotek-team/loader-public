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

    def get_raw_data(self) -> Tuple[int, int, int, int]:
        return (self.timecode, self.x, self.y, self.z)

    def scale_data(self, data_factor: float) -> None:
        self.x = int(data_factor * self.x)
        self.y = int(data_factor * self.y)
        self.z = int(data_factor * self.z)


class PositionEvents(Events):
    format = ">Hhhh"
    id: int = 0

    def add(self, timecode: int, xyz: Tuple[int, int, int]) -> None:
        self.event_list.append(PositionEvent(timecode, xyz[0], xyz[1], xyz[2]))

    def add_raw_data(self, data: Tuple[int, int, int, int]) -> None:
        self.event_list.append(PositionEvent(data[0], data[1], data[2], data[3]))
