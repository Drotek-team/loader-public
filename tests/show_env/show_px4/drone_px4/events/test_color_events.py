from loader.show_env.show_px4.drone_px4.events import (
    ColorEvent,
    ColorEvents,
)


def test_color_event_standard_case_and_method() -> None:
    color_event = ColorEvent(timecode=0, r=1, g=2, b=3, w=4)
    assert color_event.timecode == 0
    assert color_event.r == 1
    assert color_event.g == 2
    assert color_event.b == 3
    assert color_event.w == 4
    assert color_event.rgbw == (1, 2, 3, 4)
    assert color_event.get_data == [0, 1, 2, 3, 4]


def test_color_events_standard_case_and_method() -> None:
    color_events = ColorEvents()
    color_events.add_timecode_rgbw(0, (1, 2, 3, 4))
    color_events.add_timecode_rgbw(1, (5, 6, 7, 8))
    assert color_events.format_ == ">IBBBB"
    assert color_events.id_ == 1
    first_color_event = color_events.get_color_event_by_index(0)
    assert first_color_event.timecode == 0
    assert first_color_event.r == 1
    assert first_color_event.g == 2
    assert first_color_event.b == 3
    assert first_color_event.w == 4
    assert first_color_event.rgbw == (1, 2, 3, 4)
    assert first_color_event.get_data == [0, 1, 2, 3, 4]

    second_color_event = color_events.get_color_event_by_index(1)
    assert second_color_event.timecode == 1
    assert second_color_event.r == 5
    assert second_color_event.g == 6
    assert second_color_event.b == 7
    assert second_color_event.w == 8
    assert second_color_event.rgbw == (5, 6, 7, 8)
    assert second_color_event.get_data == [1, 5, 6, 7, 8]
