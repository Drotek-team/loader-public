from abc import ABC, abstractmethod
from typing import Any, List


class Event(ABC):
    timecode: int

    @property
    @abstractmethod
    def get_data(self) -> List[Any]:
        pass


class Events(ABC):
    format_: str
    id_: int

    @property
    @abstractmethod
    def generic_events(self) -> List[Event]:
        pass

    @abstractmethod
    def add_data(self, data: List[Any]) -> None:
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
