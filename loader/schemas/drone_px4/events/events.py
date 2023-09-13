import struct
from abc import ABC, abstractmethod
from typing import Any, Generic, Iterator, List, TypeVar

from .events_order import EventsType


class Event(ABC):
    frame: int

    @property
    @abstractmethod
    def get_data(self) -> List[Any]:
        pass


TEvent = TypeVar("TEvent", bound=Event)


class Events(ABC, Generic[TEvent]):
    format_: str
    id_: EventsType
    _events: List[TEvent]

    @abstractmethod
    def add_data(self, data: List[Any]) -> None:
        pass

    def __iter__(self) -> Iterator[TEvent]:
        return self._events.__iter__()

    def __getitem__(self, position_event_index: int) -> TEvent:
        return self._events[position_event_index]

    def __len__(self) -> int:
        return len(self._events)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)) and len(self) == len(other):
            return all(
                self._events[event_index] == other._events[event_index]  # noqa: SLF001
                for event_index in range(len(self._events))
            )
        return False

    @property
    def event_size(self) -> int:
        return struct.calcsize(self.format_)

    @property
    def events_size(self) -> int:
        return len(self._events) * struct.calcsize(self.format_)
