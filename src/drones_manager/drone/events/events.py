import struct
from abc import abstractclassmethod
from dataclasses import dataclass
from typing import Any, List, Tuple


@dataclass(frozen=True)
class Event:
    def __init__(self, frame: int):
        self.frame = frame

    @abstractclassmethod
    def get_values(self) -> Tuple:
        pass

    @abstractclassmethod
    def get_raw_data(self) -> Tuple:
        pass

    def scale_frame(self, frame_factor: float) -> None:
        self.frame = int(self.frame * frame_factor)

    @abstractclassmethod
    def scale_data(self, data_factor: float) -> None:
        pass


class Events:
    format: str
    id: int

    def __init__(self):
        self.event_list: List[Event] = []

    @property
    def event_size(self):
        return struct.calcsize(self.format)

    @property
    def events_size(self):
        return len(self.event_list) * struct.calcsize(self.format)

    @property
    def events(self) -> List[Event]:
        return self.event_list

    @property
    def nb_events(self) -> int:
        return len(self.event_list)

    def get_frame_by_event_index(self, event_index: int) -> int:
        return self.event_list[event_index].frame

    def get_values_by_event_index(self, event_index: int) -> Tuple:
        return self.event_list[event_index].get_values()

    def scale_frame_events(self, frame_factor: float) -> None:
        for event in self.event_list:
            event.scale_frame(frame_factor)

    def scale_data_events(self, data_factor: float) -> None:
        for event in self.event_list:
            event.scale_data(data_factor)

    @abstractclassmethod
    def add(self, frame: int, data: Any) -> None:
        pass

    @abstractclassmethod
    def add_raw_data(self, data: Tuple) -> None:
        pass
