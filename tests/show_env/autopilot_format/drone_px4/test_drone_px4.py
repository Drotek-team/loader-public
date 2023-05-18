from loader.show_env.drone_px4 import DronePx4
from loader.show_env.drone_px4.events.events_order import EventsType


def test_add_position_standard_case() -> None:
    drone = DronePx4(index=0)
    drone.add_position(timecode=0, xyz=(0, 0, 0))
    assert drone.position_events[0].get_data == [0, 0, 0, 0]
    drone.add_position(timecode=1, xyz=(1, 1, 1))
    assert drone.position_events[1].get_data == [1, 1, 1, 1]


def test_add_color_standard_case() -> None:
    drone = DronePx4(index=0)
    drone.add_color(timecode=0, rgbw=(0, 0, 0, 0))
    assert drone.color_events[0].get_data == [0, 0, 0, 0, 0]
    drone.add_color(timecode=1, rgbw=(1, 1, 1, 1))
    assert drone.color_events[1].get_data == [1, 1, 1, 1, 1]


def test_add_fire_standard_case() -> None:
    drone = DronePx4(index=0)
    drone.add_fire(timecode=0, chanel=1, duration=2)
    assert drone.fire_events[0].get_data == [0, 1, 2]
    drone.add_fire(timecode=1, chanel=3, duration=4)
    assert drone.fire_events[1].get_data == [1, 3, 4]


def test_get_events_by_index_standard_case() -> None:
    drone = DronePx4(index=0)
    assert drone.get_events_by_index(event_type=EventsType.position) == drone.position_events
    assert drone.get_events_by_index(event_type=EventsType.color) == drone.color_events
    assert drone.get_events_by_index(event_type=EventsType.fire) == drone.fire_events


def test_events_list_standard_case() -> None:
    drone = DronePx4(index=0)
    assert drone.events_dict == {
        EventsType.position: drone.position_events,
        EventsType.color: drone.color_events,
        EventsType.fire: drone.fire_events,
    }


def test_non_empty_events_list_standard_case() -> None:
    drone = DronePx4(index=0)
    assert drone.non_empty_events_list == []
    drone.add_position(timecode=0, xyz=(0, 0, 0))
    assert drone.non_empty_events_list == [drone.position_events]
    drone.add_color(timecode=0, rgbw=(0, 0, 0, 0))
    assert drone.non_empty_events_list == [drone.position_events, drone.color_events]
    drone.add_fire(timecode=0, chanel=0, duration=0)
    assert drone.non_empty_events_list == [
        drone.position_events,
        drone.color_events,
        drone.fire_events,
    ]


def test___eq___standard_case() -> None:
    drone = DronePx4(index=0)
    assert drone == drone
    other_drone = DronePx4(index=0)
    assert drone == other_drone
    drone.add_position(timecode=0, xyz=(0, 0, 0))
    assert drone != other_drone
    other_drone.add_position(timecode=0, xyz=(0, 0, 0))
    assert drone == other_drone
    drone.add_color(timecode=0, rgbw=(0, 0, 0, 0))
    assert drone != other_drone
    other_drone.add_color(timecode=0, rgbw=(0, 0, 0, 0))
    assert drone == other_drone
    drone.add_fire(timecode=0, chanel=0, duration=0)
    assert drone != other_drone
    other_drone.add_fire(timecode=0, chanel=0, duration=0)
    assert drone == other_drone


def test___eq___with_other_type() -> None:
    drone = DronePx4(index=0)
    assert drone != 0
