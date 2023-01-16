from enum import Enum


class EventsType(Enum):
    position = "position"
    color = "color"
    fire = "fire"


EVENTS_ID = {
    EventsType.position: 0,
    EventsType.color: 1,
    EventsType.fire: 2,
}
