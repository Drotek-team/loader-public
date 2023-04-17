from dataclasses import dataclass
from typing import Any, List, Tuple

from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)

from .events import Event, Events
from .events_order import EventsType


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
    def __init__(self) -> None:
        self.format_ = JSON_BINARY_PARAMETER.fire_event_format
        self.id_ = EventsType.fire
        # Had to pass with the init because python mutable defaults are the source of all evil
        # https://florimond.dev/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
        self._events = []

    def add_timecode_chanel_duration(
        self,
        timecode: int,
        chanel: int,
        duration: int,
    ) -> None:
        self._events.append(
            FireEvent(timecode=timecode, chanel=chanel, duration=duration),
        )

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            FireEvent(timecode=data[0], chanel=data[1], duration=data[2]),
        )

    def get_fire_event_by_index(self, index: int) -> FireEvent:
        fire_event_data = self._events[index].get_data
        return FireEvent(
            timecode=fire_event_data[0],
            chanel=fire_event_data[1],
            duration=fire_event_data[2],
        )

    @property
    def specific_events(self) -> List[FireEvent]:
        return [
            self.get_fire_event_by_index(event_index) for event_index in range(len(self._events))
        ]
