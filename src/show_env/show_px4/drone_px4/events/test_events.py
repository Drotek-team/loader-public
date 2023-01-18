from typing import Any, List

from .events import Event, Events


class DummyEvent(Event):
    def __init__(self):
        self.timecode = 5

    @property
    def get_data(self) -> List[Any]:
        return [self.timecode]


class DummyEvents(Events):
    def __init__(self):
        self.format_ = ">Ihhh"
        self.id_ = 0
        self._events: List[Event] = []

    def add_data(self, data: List[Any]) -> None:
        self._events.append(DummyEvent())


def test_events_standard_case_and_method():
    events = DummyEvents()
    assert events.event_size == 10
    assert events.events_size == 0
    assert len(events) == 0
    assert events == DummyEvents()
