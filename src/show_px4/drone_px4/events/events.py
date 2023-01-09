from abc import ABC, abstractmethod
from typing import List, Tuple


class Event(ABC):
    frame: int

    @abstractmethod
    def get_data(self) -> Tuple:
        pass


class Events(ABC):
    format: str
    id: int
    events: List[Event]

    @abstractmethod
    def add_data(self, data: Tuple) -> None:
        pass

    @property
    def event_size(self) -> int:
        pass

    @property
    def events_size(self) -> int:
        pass

    @property
    def nb_events(self) -> int:
        pass

    @abstractmethod
    def get_frame_by_event_index(self, event_index: int) -> int:
        pass
