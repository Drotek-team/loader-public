from typing import Any, List

from loader.show_env.show_px4.drone_px4.events.events import Event, Events


class DummyEvent(Event):
    def __init__(self) -> None:
        self.timecode = 5

    @property
    def get_data(self) -> List[Any]:
        return [self.timecode]


class DummyEvents(Events):
    def __init__(self) -> None:
        self.format_ = ">Ihhh"
        self.id_ = 0
        self._events: List[Event] = []

    def add_data(self, data: List[Any]) -> None:  # noqa: ARG002
        self._events.append(DummyEvent())


def test_events_standard_case_and_method() -> None:
    events = DummyEvents()
    assert events.event_size == 10
    assert events.events_size == 0
    assert len(events) == 0
    assert events == DummyEvents()
