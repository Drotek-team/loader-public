import pytest

from .drone_px4 import DronePx4


def test_add_position_standard_case() -> None:
    drone = DronePx4(index=0)
    drone.add_position(timecode=0, xyz=(0, 0, 0))
    assert drone.position_events.events[0].timecode == 0
    assert drone.position_events.events[0].xyz == (0, 0, 0)
    drone.add_position(timecode=1, xyz=(1, 1, 1))
    assert drone.position_events.events[1].timecode == 1
    assert drone.position_events.events[1].xyz == (1, 1, 1)
    drone.add_position(timecode=2, xyz=(2, 2, 2))
    assert drone.position_events.events[2].timecode == 2
    assert drone.position_events.events[2].xyz == (2, 2, 2)


def test_add_color_standard_case():
    drone = DronePx4(index=0)
    drone.add_color(timecode=0, rgbw=(0, 0, 0, 0))
    assert drone.color_events.events[0].timecode == 0
    assert drone.color_events.events[0].rgbw == (0, 0, 0, 0)
    drone.add_color(timecode=1, rgbw=(1, 1, 1, 1))
    assert drone.color_events.events[1].timecode == 1
    assert drone.color_events.events[1].rgbw == (1, 1, 1, 1)
    drone.add_color(timecode=2, rgbw=(2, 2, 2, 2))
    assert drone.color_events.events[2].timecode == 2
    assert drone.color_events.events[2].rgbw == (2, 2, 2, 2)


def test_add_fire_standard_case():
    drone = DronePx4(index=0)
    drone.add_fire(timecode=0, chanel=0, duration_frame=0)
    assert drone.fire_events.events[0].timecode == 0
    assert drone.fire_events.events[0].chanel == 0
    assert drone.fire_events.events[0].duration == 0
    drone.add_fire(timecode=1, chanel=1, duration_frame=1)
    assert drone.fire_events.events[1].timecode == 1
    assert drone.fire_events.events[1].chanel == 1
    assert drone.fire_events.events[1].duration == 1
    drone.add_fire(timecode=2, chanel=2, duration_frame=2)
    assert drone.fire_events.events[2].timecode == 2
    assert drone.fire_events.events[2].chanel == 2
    assert drone.fire_events.events[2].duration == 2


def test_get_events_by_index_standard_case():
    drone = DronePx4(index=0)
    assert drone.get_events_by_index(event_index=0) == drone.position_events
    assert drone.get_events_by_index(event_index=1) == drone.color_events
    assert drone.get_events_by_index(event_index=2) == drone.fire_events


def test_get_events_by_index_out_of_range():
    drone = DronePx4(index=0)
    with pytest.raises(IndexError):
        drone.get_events_by_index(event_index=-1)
    with pytest.raises(IndexError):
        drone.get_events_by_index(event_index=3)


def test_events_list_standard_case():
    drone = DronePx4(index=0)
    assert drone.events_list == [
        drone.position_events,
        drone.color_events,
        drone.fire_events,
    ]


def test_non_empty_events_list_standard_case():
    drone = DronePx4(index=0)
    assert drone.non_empty_events_list == []
    drone.add_position(timecode=0, xyz=(0, 0, 0))
    assert drone.non_empty_events_list == [drone.position_events]
    drone.add_color(timecode=0, rgbw=(0, 0, 0, 0))
    assert drone.non_empty_events_list == [drone.position_events, drone.color_events]
    drone.add_fire(timecode=0, chanel=0, duration_frame=0)
    assert drone.non_empty_events_list == [
        drone.position_events,
        drone.color_events,
        drone.fire_events,
    ]
