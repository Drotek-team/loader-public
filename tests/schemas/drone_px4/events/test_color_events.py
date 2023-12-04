import pytest
from loader.parameters.json_binary_parameters import MagicNumber
from loader.schemas.drone_px4.events import ColorEvent, ColorEvents


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_color_event_standard_case_and_method(magic_number: MagicNumber) -> None:
    color_event = ColorEvent(frame=0, r=1, g=2, b=3, w=4)
    assert color_event.frame == 0
    assert color_event.r == 1
    assert color_event.g == 2
    assert color_event.b == 3
    assert color_event.w == 4
    assert color_event.rgbw == (1, 2, 3, 4)
    assert color_event.get_data(magic_number) == [
        0,
        1,
        2,
        3,
        4 if magic_number == MagicNumber.v1 else 2,
    ]


@pytest.mark.parametrize("magic_number", list(MagicNumber))
def test_color_events_standard_case_and_method(magic_number: MagicNumber) -> None:
    color_events = ColorEvents(magic_number)
    color_events.add_timecode_rgbw(0, (1, 2, 3, 4))
    color_events.add_timecode_rgbw(1, (5, 6, 7, 8))
    assert color_events.id_ == 1
    first_color_event = color_events[0]
    assert first_color_event.frame == 0
    assert first_color_event.r == 1
    assert first_color_event.g == 2
    assert first_color_event.b == 3
    assert first_color_event.w == 4
    assert first_color_event.rgbw == (1, 2, 3, 4)
    assert first_color_event.get_data(magic_number) == [
        0,
        1,
        2,
        3,
        4 if magic_number == MagicNumber.v1 else 2,
    ]

    second_color_event = color_events[1]
    assert second_color_event.frame == 1
    assert second_color_event.r == 5
    assert second_color_event.g == 6
    assert second_color_event.b == 7
    assert second_color_event.w == 8
    assert second_color_event.rgbw == (5, 6, 7, 8)
    assert second_color_event.get_data(magic_number) == [
        42 if magic_number == MagicNumber.v1 else 1,
        5,
        6,
        7,
        8 if magic_number == MagicNumber.v1 else 4,
    ]
