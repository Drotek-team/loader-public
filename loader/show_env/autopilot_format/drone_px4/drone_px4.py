from typing import List, Tuple

from .events import ColorEvents, Events, EventsType, FireEvents, PositionEvents


class DronePx4:
    def __init__(self, index: int) -> None:
        self.index = index
        self.position_events = PositionEvents()
        self.color_events = ColorEvents()
        self.fire_events = FireEvents()
        self.events_dict = {
            events.id_: events
            for events in [self.position_events, self.color_events, self.fire_events]
        }

    def __eq__(self, other_drone_px4: object) -> bool:
        if not isinstance(other_drone_px4, DronePx4):
            return False
        return self.index == self.index and self.events_dict == other_drone_px4.events_dict

    def add_position(self, timecode: int, xyz: Tuple[int, int, int]) -> None:
        self.position_events.add_timecode_xyz(timecode, xyz)

    def add_color(self, timecode: int, rgbw: Tuple[int, int, int, int]) -> None:
        self.color_events.add_timecode_rgbw(timecode, rgbw)

    def add_fire(self, timecode: int, chanel: int, duration_frame: int) -> None:
        self.fire_events.add_timecode_chanel_duration(timecode, chanel, duration_frame)

    def get_events_by_index(self, event_type: EventsType) -> Events:
        return self.events_dict[event_type]

    @property
    def non_empty_events_list(self) -> List[Events]:
        return [events for events in self.events_dict.values() if len(events) != 0]
