from .fire_events import FireEvent, FireEvents


def test_fire_event_standard_case_and_method():
    fire_event = FireEvent(timecode=0, chanel=1, duration=2)
    assert fire_event.timecode == 0
    assert fire_event.chanel == 1
    assert fire_event.duration == 2
    assert fire_event.chanel_duration == (1, 2)
    assert fire_event.get_data == [0, 1, 2]


def test_fire_events_standard_case_and_method():
    fire_events = FireEvents()
    fire_events.add_timecode_chanel_duration(0, 1, 2)
    fire_events.add_timecode_chanel_duration(1, 3, 4)
    assert fire_events.format_ == ">IBB"
    assert fire_events.id_ == 2
    assert fire_events.events[0].timecode == 0
    assert fire_events.events[0].chanel == 1
    assert fire_events.events[0].duration == 2
    assert fire_events.events[0].chanel_duration == (1, 2)
    assert fire_events.events[0].get_data == [0, 1, 2]
    assert fire_events.events[1].timecode == 1
    assert fire_events.events[1].chanel == 3
    assert fire_events.events[1].duration == 4
    assert fire_events.events[1].chanel_duration == (3, 4)
    assert fire_events.events[1].get_data == [1, 3, 4]
    assert fire_events.event_size == 6
    assert fire_events.events_size == 12
    assert fire_events.nb_events == 2
    assert fire_events.generic_events == fire_events.events
