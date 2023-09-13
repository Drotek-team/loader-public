from loader.schemas.drone_px4.events import FireEvent, FireEvents


def test_fire_event_standard_case_and_method() -> None:
    fire_event = FireEvent(frame=0, channel=1, duration=2)
    assert fire_event.frame == 0
    assert fire_event.channel == 1
    assert fire_event.duration == 2
    assert fire_event.channel_duration == (1, 2)
    assert fire_event.get_data == [0, 1, 2]


def test_fire_events_standard_case_and_method() -> None:
    fire_events = FireEvents()
    fire_events.add_timecode_channel_duration(0, 1, 2)
    fire_events.add_timecode_channel_duration(1, 3, 4)
    assert fire_events.format_ == ">IBB"
    assert fire_events.id_ == 2
    first_fire_event = fire_events[0]
    assert first_fire_event.frame == 0
    assert first_fire_event.channel == 1
    assert first_fire_event.duration == 2
    assert first_fire_event.channel_duration == (1, 2)
    assert first_fire_event.get_data == [0, 1, 2]

    second_fire_event = fire_events[1]
    assert second_fire_event.frame == 1
    assert second_fire_event.channel == 3
    assert second_fire_event.duration == 4
    assert second_fire_event.channel_duration == (3, 4)
    assert second_fire_event.get_data == [42, 3, 4]
