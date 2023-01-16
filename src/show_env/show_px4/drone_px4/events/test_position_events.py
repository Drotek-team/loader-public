from .position_events import PositionEvent, PositionEvents


def test_position_event_standard_case_and_method():
    position_event = PositionEvent(timecode=0, x=1, y=2, z=3)
    assert position_event.timecode == 0
    assert position_event.x == 1
    assert position_event.y == 2
    assert position_event.z == 3
    assert position_event.xyz == (1, 2, 3)
    assert position_event.get_data == [0, 1, 2, 3]


def test_position_events_standard_case_and_method():
    position_events = PositionEvents()
    position_events.add_timecode_xyz(0, (1, 2, 3))
    position_events.add_timecode_xyz(1, (4, 5, 6))
    assert position_events.format_ == ">Ihhh"
    assert position_events.id_ == 0
    assert position_events.events[0].timecode == 0
    assert position_events.events[0].x == 1
    assert position_events.events[0].y == 2
    assert position_events.events[0].z == 3
    assert position_events.events[0].xyz == (1, 2, 3)
    assert position_events.events[0].get_data == [0, 1, 2, 3]
    assert position_events.events[1].timecode == 1
    assert position_events.events[1].x == 4
    assert position_events.events[1].y == 5
    assert position_events.events[1].z == 6
    assert position_events.events[1].xyz == (4, 5, 6)
    assert position_events.events[1].get_data == [1, 4, 5, 6]
    assert position_events.event_size == 10
    assert position_events.events_size == 20
    assert position_events.nb_events == 2
    assert position_events.generic_events == position_events.events
