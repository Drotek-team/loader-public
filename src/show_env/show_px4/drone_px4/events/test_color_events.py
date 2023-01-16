from .color_events import ColorEvent, ColorEvents


def test_color_event_standard_case_and_method():
    color_event = ColorEvent(timecode=0, r=1, g=2, b=3, w=4)
    assert color_event.timecode == 0
    assert color_event.r == 1
    assert color_event.g == 2
    assert color_event.b == 3
    assert color_event.w == 4
    assert color_event.rgbw == (1, 2, 3, 4)
    assert color_event.get_data == [0, 1, 2, 3, 4]


def test_color_events_standard_case_and_method():
    color_events = ColorEvents()
    color_events.add_timecode_rgbw(0, (1, 2, 3, 4))
    color_events.add_timecode_rgbw(1, (5, 6, 7, 8))
    assert color_events.format_ == ">IBBBB"
    assert color_events.id_ == 1
    assert color_events.events[0].timecode == 0
    assert color_events.events[0].r == 1
    assert color_events.events[0].g == 2
    assert color_events.events[0].b == 3
    assert color_events.events[0].w == 4
    assert color_events.events[0].rgbw == (1, 2, 3, 4)
    assert color_events.events[0].get_data == [0, 1, 2, 3, 4]
    assert color_events.events[1].timecode == 1
    assert color_events.events[1].r == 5
    assert color_events.events[1].g == 6
    assert color_events.events[1].b == 7
    assert color_events.events[1].w == 8
    assert color_events.events[1].rgbw == (5, 6, 7, 8)
    assert color_events.events[1].get_data == [1, 5, 6, 7, 8]
    assert color_events.event_size == 8
    assert color_events.events_size == 16
    assert color_events.nb_events == 2
    assert color_events.generic_events == color_events.events
