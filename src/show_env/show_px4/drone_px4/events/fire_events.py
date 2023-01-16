import struct
from dataclasses import dataclass
from typing import Any, List, Tuple

from .events import Event, Events
from .events_order import EVENTS_ID, EventsType


@dataclass(frozen=True)
class FireEvent(Event):
    timecode: int  # time frame associate to the "fps_px4" parameter
    chanel: int  # chanel of the fire event
    duration: int  # duration of the fire event in timecode

    @property
    def chanel_duration(self) -> Tuple[int, int]:
        return (self.chanel, self.duration)

    @property
    def get_data(self) -> List[Any]:
        return [self.timecode, self.chanel, self.duration]


class FireEvents(Events):
    format_ = ">IBB"

    def __init__(self):
        self._events: List[FireEvent] = []
        self.id_ = EVENTS_ID[EventsType.fire]

    def __getitem__(self, fire_event_index: int):
        return self._events[fire_event_index]

    def __len__(self) -> int:
        return len(self._events)

    @property
    def generic_events(self) -> List[Event]:
        return self._events  # type: ignore[I an pretty this is a bug from pylance, the typing works if the function return FireEvent with a Event typing]

    def add_timecode_chanel_duration(
        self, timecode: int, chanel: int, duration: int
    ) -> None:
        self._events.append(
            FireEvent(timecode=timecode, chanel=chanel, duration=duration)
        )

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            FireEvent(timecode=data[0], chanel=data[1], duration=data[2])
        )

    @property
    def event_size(self):
        return struct.calcsize(self.format_)

    @property
    def events_size(self):
        return len(self._events) * struct.calcsize(self.format_)

    @property
    def nb_events(self) -> int:
        return len(self._events)
