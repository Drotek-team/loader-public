from typing import List, Tuple

from .events import ColorEvents, Events, EventsType, FireEvents, PositionEvents


# TODO: en reparler pour généraliser nouveau drone
class DronePx4:
    def __init__(self, index: int) -> None:
        self.index = index
        self.position_events = PositionEvents()
        self.color_events = ColorEvents()
        self.fire_events = FireEvents()

    def __eq__(self, other_drone_px4: object) -> bool:
        if isinstance(other_drone_px4, DronePx4):
            return self.index == self.index and all(
                events == other_events
                for events, other_events in zip(
                    self.events_list,
                    other_drone_px4.events_list,
                )
            )
        return False

    def add_position(self, timecode: int, xyz: Tuple[int, int, int]) -> None:
        self.position_events.add_timecode_xyz(timecode, xyz)

    def add_color(self, timecode: int, rgbw: Tuple[int, int, int, int]) -> None:
        self.color_events.add_timecode_rgbw(timecode, rgbw)

    def add_fire(self, timecode: int, chanel: int, duration_frame: int) -> None:
        self.fire_events.add_timecode_chanel_duration(timecode, chanel, duration_frame)

    # TODO: Improve this method
    def get_events_by_index(self, event_type: EventsType) -> Events:
        events_enum = {events.id_: events for events in self.events_list}
        return events_enum[event_type]

    @property
    def events_list(self) -> List[Events]:
        return [self.position_events, self.color_events, self.fire_events]

    @property
    def non_empty_events_list(self) -> List[Events]:
        return [events for events in self.events_list if events]
