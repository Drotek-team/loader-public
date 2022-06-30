import struct
from abc import abstractclassmethod
from dataclasses import dataclass
from typing import List, Tuple


@dataclass(frozen=True)
class Event:
    def __init__(self, timecode: int):
        self.timecode = timecode

    @abstractclassmethod
    def get_values(self) -> Tuple:
        pass


class Events:
    format: str
    id: int

    def __init__(self):
        self.event_list: List[Event] = []

    def event_size(self):
        return struct.calcsize(self.format)

    def events_size(self):
        return len(self.event_list) * struct.calcsize(self.format)

    @property
    def events(self) -> List[Event]:
        return self.event_list

    @property
    def nb_events(self) -> int:
        return len(self.event_list)

    def get_timecode_by_event_index(self, event_index: int) -> int:
        return self.event_list[event_index].timecode

    def get_values_by_event_index(self, event_index: int) -> Tuple:
        return self.event_list[event_index].get_values()

    @abstractclassmethod
    def add(self, timecode: int, data) -> None:
        pass

    def encode(self) -> bytearray:
        event_size = self.event_size()
        binary = bytearray(event_size * len(self.event_list))
        for cpt_event, event_data in enumerate(self.event_list):
            binary[cpt_event * event_size : (cpt_event + 1) * event_size] = struct.pack(
                self.format, *event_data.get_values()
            )
        return binary

    # def decode(self, binary, **parameter):
    #     index = 0
    #     self._events = []
    #     if len(binary) % self._size_event != 0:
    #         raise EventsSizeError
    #     for _ in range(len(binary) // self._size_event):
    #         event = struct.unpack(
    #             self._format, binary[index : index + self._size_event]
    #         )
    #         self.add(*self._transform(*event, **parameter))
    #         index += self._size_event
