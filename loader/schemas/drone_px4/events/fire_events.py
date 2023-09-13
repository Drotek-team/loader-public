from dataclasses import dataclass
from typing import Any, List, Tuple

from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS

from .events import Event, Events
from .events_order import EventsType


@dataclass(frozen=True)
class FireEvent(Event):
    timecode: int  # time frame associate to the "fps_px4" parameter
    channel: int  # channel of the fire event
    duration: int  # duration of the fire event in milliseconds

    @property
    def channel_duration(self) -> Tuple[int, int]:
        return (self.channel, self.duration)

    @property
    def get_data(self) -> List[Any]:
        return [self.timecode, self.channel, self.duration]


class FireEvents(Events[FireEvent]):
    def __init__(self) -> None:
        self.format_ = JSON_BINARY_PARAMETERS.fire_event_format
        self.id_ = EventsType.fire
        # Had to pass with the init because python mutable defaults are the source of all evil
        # https://florimond.dev/en/posts/2018/08/python-mutable-defaults-are-the-source-of-all-evil/
        self._events = []

    def add_timecode_channel_duration(
        self,
        frame: int,
        channel: int,
        duration: int,
    ) -> None:
        self._events.append(
            FireEvent(
                timecode=JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(frame),
                channel=channel,
                duration=duration,
            ),
        )

    def add_data(self, data: List[Any]) -> None:
        self._events.append(
            FireEvent(timecode=data[0], channel=data[1], duration=data[2]),
        )
