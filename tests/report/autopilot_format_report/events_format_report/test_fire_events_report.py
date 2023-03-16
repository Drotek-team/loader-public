import pytest
from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.report.autopilot_format_report.events_format_report import (
    DurationChanelInfraction,
    FireEventsReport,
)
from loader.report.base import get_report_validation
from loader.show_env.autopilot_format.drone_px4.events import FireEvents


@pytest.fixture
def valid_fire_events() -> FireEvents:
    fire_events = FireEvents()
    fire_events.add_timecode_chanel_duration(
        timecode=JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame,
        ),
        chanel=0,
        duration=0,
    )
    fire_events.add_timecode_chanel_duration(
        timecode=JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame + 1,
        ),
        chanel=1,
        duration=0,
    )
    fire_events.add_timecode_chanel_duration(
        timecode=JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame + 2,
        ),
        chanel=2,
        duration=0,
    )
    return fire_events


def test_valid_fire_events_report(
    valid_fire_events: FireEvents,
) -> None:
    fire_events_report = FireEventsReport.generate(
        valid_fire_events,
    )
    assert get_report_validation(fire_events_report)


def test_invalid_fire_events_chanel_value_report(
    valid_fire_events: FireEvents,
) -> None:
    valid_fire_events.add_timecode_chanel_duration(
        JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
        JSON_BINARY_PARAMETER.fire_chanel_value_bound.maximal + 1,
        0,
    )
    fire_events_report = FireEventsReport.generate(
        valid_fire_events,
    )
    assert fire_events_report is not None
    assert len(fire_events_report.duration_chanel_infractions) == 1
    assert fire_events_report.duration_chanel_infractions[
        0
    ] == DurationChanelInfraction(
        event_index=3,
        value=3,
        value_min=0,
        value_max=2,
    )


def test_invalid_fire_events_duration_value_report(
    valid_fire_events: FireEvents,
) -> None:
    valid_fire_events.add_timecode_chanel_duration(
        JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
        0,
        JSON_BINARY_PARAMETER.fire_duration_value_bound.maximal + 1,
    )
    fire_events_report = FireEventsReport.generate(
        valid_fire_events,
    )
    assert fire_events_report is not None
    assert len(fire_events_report.duration_chanel_infractions) == 1
    assert fire_events_report.duration_chanel_infractions[
        0
    ] == DurationChanelInfraction(
        event_index=3,
        value=256,
        value_min=0,
        value_max=255,
    )
