from loader.schemas.drone_px4 import DronePx4
from loader.schemas.drone_px4.events.events_order import EventsType
from loader.schemas.drone_px4.events.magic_number import MagicNumber


def test_add_position_standard_case() -> None:
    drone = DronePx4(index=0, magic_number=MagicNumber.old)
    drone.add_position(frame=0, xyz=(0, 0, 0))
    assert drone.position_events[0].get_data(MagicNumber.old) == [0, 0, 0, 0]
    drone.add_position(frame=1, xyz=(1, 1, 1))
    assert drone.position_events[1].get_data(MagicNumber.old) == [42, 1, 1, 1]


def test_add_color_standard_case() -> None:
    drone = DronePx4(index=0, magic_number=MagicNumber.old)
    drone.add_color(frame=0, rgbw=(0, 0, 0, 0))
    assert drone.color_events[0].get_data(MagicNumber.old) == [0, 0, 0, 0, 0]
    drone.add_color(frame=1, rgbw=(1, 1, 1, 1))
    assert drone.color_events[1].get_data(MagicNumber.old) == [42, 1, 1, 1, 1]


def test_add_fire_standard_case() -> None:
    drone = DronePx4(index=0, magic_number=MagicNumber.old)
    drone.add_fire(frame=0, channel=1, duration=2)
    assert drone.fire_events[0].get_data(MagicNumber.old) == [0, 1, 2]
    drone.add_fire(frame=1, channel=3, duration=4)
    assert drone.fire_events[1].get_data(MagicNumber.old) == [42, 3, 4]


def test_get_events_by_index_standard_case() -> None:
    drone = DronePx4(index=0, magic_number=MagicNumber.old)
    assert drone.get_events_by_index(event_type=EventsType.position) == drone.position_events
    assert drone.get_events_by_index(event_type=EventsType.color) == drone.color_events
    assert drone.get_events_by_index(event_type=EventsType.fire) == drone.fire_events


def test_events_list_standard_case() -> None:
    drone = DronePx4(index=0, magic_number=MagicNumber.old)
    assert drone.events_dict == {
        EventsType.position: drone.position_events,
        EventsType.color: drone.color_events,
        EventsType.fire: drone.fire_events,
    }


def test_non_empty_events_list_standard_case() -> None:
    drone = DronePx4(index=0, magic_number=MagicNumber.old)
    assert drone.non_empty_events_list == []
    drone.add_position(frame=0, xyz=(0, 0, 0))
    assert drone.non_empty_events_list == [drone.position_events]
    drone.add_color(frame=0, rgbw=(0, 0, 0, 0))
    assert drone.non_empty_events_list == [drone.position_events, drone.color_events]
    drone.add_fire(frame=0, channel=0, duration=0)
    assert drone.non_empty_events_list == [
        drone.position_events,
        drone.color_events,
        drone.fire_events,
    ]


def test___eq___standard_case() -> None:
    drone = DronePx4(index=0, magic_number=MagicNumber.old)
    assert drone == drone  # noqa: PLR0124
    other_drone = DronePx4(index=0, magic_number=MagicNumber.old)
    assert drone == other_drone
    drone.add_position(frame=0, xyz=(0, 0, 0))
    assert drone != other_drone
    other_drone.add_position(frame=0, xyz=(0, 0, 0))
    assert drone == other_drone
    drone.add_color(frame=0, rgbw=(0, 0, 0, 0))
    assert drone != other_drone
    other_drone.add_color(frame=0, rgbw=(0, 0, 0, 0))
    assert drone == other_drone
    drone.add_fire(frame=0, channel=0, duration=0)
    assert drone != other_drone
    other_drone.add_fire(frame=0, channel=0, duration=0)
    assert drone == other_drone


def test___eq___with_other_type() -> None:
    drone = DronePx4(index=0, magic_number=MagicNumber.old)
    assert drone != 0
