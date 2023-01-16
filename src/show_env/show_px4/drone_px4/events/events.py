import struct
from abc import ABC, abstractmethod
from typing import Any, List


class Event(ABC):
    timecode: int

    @property
    @abstractmethod
    def get_data(self) -> List[Any]:
        pass


class Events:
    format_: str
    id_: int
    _events: List[Event]

    @abstractmethod
    def add_data(self, data: List[Any]) -> None:
        pass

    # TODO: test these methods, this implies that the structure of the init is different: need to do a super()
    def __iter__(self):
        yield from self._events

    def __getitem__(self, position_event_index: int):
        return self._events[position_event_index]

    def __len__(self) -> int:
        return len(self._events)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Events) and len(self) == len(other):
            return all(
                [
                    self._events[event_index] == other._events[event_index]
                    for event_index in range(len(self._events))
                ]
            )
        return False

    @property
    def event_size(self):
        return struct.calcsize(self.format_)

    @property
    def events_size(self):
        return len(self._events) * struct.calcsize(self.format_)
