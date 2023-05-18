from loader.show_env.drone_px4.events import (
    PositionEvent,
    PositionEvents,
)


def test_position_event_standard_case_and_method() -> None:
    position_event = PositionEvent(timecode=0, x=1, y=2, z=3)
    assert position_event.timecode == 0
    assert position_event.x == 1
    assert position_event.y == 2
    assert position_event.z == 3
    assert position_event.xyz == (1, 2, 3)
    assert position_event.get_data == [0, 1, 2, 3]


def test_position_events_standard_case_and_method() -> None:
    position_events = PositionEvents()
    position_events.add_timecode_xyz(0, (1, 2, 3))
    position_events.add_timecode_xyz(1, (4, 5, 6))
    assert position_events.format_ == ">Ihhh"
    assert position_events.id_ == 0
    first_position_event = position_events.get_position_event_by_index(0)
    assert first_position_event.timecode == 0
    assert first_position_event.x == 1
    assert first_position_event.y == 2
    assert first_position_event.z == 3
    assert first_position_event.xyz == (1, 2, 3)
    assert first_position_event.get_data == [0, 1, 2, 3]

    second_position_event = position_events.get_position_event_by_index(1)
    assert second_position_event.timecode == 1
    assert second_position_event.x == 4
    assert second_position_event.y == 5
    assert second_position_event.z == 6
    assert second_position_event.xyz == (4, 5, 6)
    assert second_position_event.get_data == [1, 4, 5, 6]
