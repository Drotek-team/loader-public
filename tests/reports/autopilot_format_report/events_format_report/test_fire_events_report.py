import pytest
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.reports import EventsReport
from loader.reports.autopilot_format_report.events_format_report.events_format_infractions import (
    BoundaryInfraction,
)
from loader.schemas.drone_px4.events import FireEvents


@pytest.fixture
def valid_fire_events() -> FireEvents:
    fire_events = FireEvents()
    fire_events.add_timecode_channel_duration(
        timecode=JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETERS.show_start_frame,
        ),
        channel=0,
        duration=0,
    )
    fire_events.add_timecode_channel_duration(
        timecode=JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETERS.show_start_frame + 1,
        ),
        channel=1,
        duration=0,
    )
    fire_events.add_timecode_channel_duration(
        timecode=JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETERS.show_start_frame + 2,
        ),
        channel=2,
        duration=0,
    )
    return fire_events


def test_valid_fire_events_report(
    valid_fire_events: FireEvents,
) -> None:
    fire_events_report = EventsReport.generate(
        valid_fire_events,
    )
    assert not len(fire_events_report)


def test_invalid_fire_events_channel_value_report(
    valid_fire_events: FireEvents,
) -> None:
    valid_fire_events.add_timecode_channel_duration(
        JSON_BINARY_PARAMETERS.timecode_value_bound.maximal,
        JSON_BINARY_PARAMETERS.fire_channel_value_bound.maximal + 1,
        0,
    )
    fire_events_report = EventsReport.generate(
        valid_fire_events,
    )
    assert len(fire_events_report)
    assert len(fire_events_report.boundary_infractions) == 1
    assert fire_events_report.boundary_infractions["channel"][0] == BoundaryInfraction(
        event_index=3,
        value=3,
    )


def test_invalid_fire_events_duration_value_report(
    valid_fire_events: FireEvents,
) -> None:
    valid_fire_events.add_timecode_channel_duration(
        JSON_BINARY_PARAMETERS.timecode_value_bound.maximal,
        0,
        JSON_BINARY_PARAMETERS.fire_duration_value_bound.maximal + 1,
    )
    fire_events_report = EventsReport.generate(
        valid_fire_events,
    )
    assert len(fire_events_report)
    assert len(fire_events_report.boundary_infractions) == 1
    assert fire_events_report.boundary_infractions["duration"][0] == BoundaryInfraction(
        event_index=3,
        value=256,
    )
