from typing import Any

from loader.parameters.json_binary_parameters import MagicNumber
from loader.schemas.drone_px4.events import Event, Events
from loader.schemas.drone_px4.events.events_order import EventsType


class DummyEvent(Event):  # pragma: no cover
    def __init__(self) -> None:
        self.frame = 5

    def get_data(self, magic_number: MagicNumber) -> list[Any]:  # noqa: ARG002
        return [self.frame]


class DummyEvents(Events[DummyEvent]):  # pragma: no cover
    def __init__(self) -> None:
        self.format_ = ">Ihhh"
        self.id_ = EventsType.position
        self._events = []

    def add_data(self, data: list[Any]) -> None:  # noqa: ARG002
        self._events.append(DummyEvent())


def test_events_standard_case_and_method() -> None:
    events = DummyEvents()
    assert events.event_size == 10
    assert events.events_size == 0
    assert len(events) == 0
    assert events == DummyEvents()
