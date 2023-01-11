from abc import ABC, abstractmethod
from typing import List, Tuple


class Event(ABC):
    timecode: int

    @abstractmethod
    def get_data(self) -> Tuple:
        pass


class Events(ABC):
    format_: str
    id_: int
    events: List[Event]

    @abstractmethod
    def add_data(self, data: Tuple) -> None:
        pass

    @property
    @abstractmethod
    def event_size(self) -> int:
        pass

    @property
    @abstractmethod
    def events_size(self) -> int:
        pass

    @property
    @abstractmethod
    def nb_events(self) -> int:
        pass

    @abstractmethod
    def get_frame_by_event_index(self, event_index: int) -> int:
        pass
