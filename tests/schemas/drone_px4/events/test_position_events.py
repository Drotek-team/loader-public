import pytest
from loader.parameters.json_binary_parameters import MagicNumber
from loader.schemas.drone_px4.events import PositionEvent, PositionEvents


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_position_event_standard_case_and_method(magic_number: MagicNumber) -> None:
    position_event = PositionEvent(frame=0, x=1, y=2, z=3)
    assert position_event.frame == 0
    assert position_event.x == 1
    assert position_event.y == 2
    assert position_event.z == 3
    assert position_event.xyz == (1, 2, 3)
    assert position_event.get_data(magic_number) == [0, 1, 2, 3]


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_position_events_standard_case_and_method(magic_number: MagicNumber) -> None:
    position_events = PositionEvents(magic_number)
    position_events.add_timecode_xyz(0, (1, 2, 3))
    position_events.add_timecode_xyz(1, (4, 5, 6))
    assert position_events.id_ == 0
    first_position_event = position_events[0]
    assert first_position_event.frame == 0
    assert first_position_event.x == 1
    assert first_position_event.y == 2
    assert first_position_event.z == 3
    assert first_position_event.xyz == (1, 2, 3)
    assert first_position_event.get_data(magic_number) == [0, 1, 2, 3]

    second_position_event = position_events[1]
    assert second_position_event.frame == 1
    assert second_position_event.x == 4
    assert second_position_event.y == 5
    assert second_position_event.z == 6
    assert second_position_event.xyz == (4, 5, 6)
    assert second_position_event.get_data(magic_number) == [
        42 if magic_number == MagicNumber.old else 1,
        4,
        5,
        6,
    ]
