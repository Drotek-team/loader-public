import pytest
from loader.check.show_px4_check.events_format_check import (
    IntegerBoundaryInfraction,
    get_fire_events_report,
)
from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.report import get_base_report_validation
from loader.show_env.show_px4.drone_px4.events.fire_events import FireEvents


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


def test_valid_fire_events_check(
    valid_fire_events: FireEvents,
) -> None:
    fire_events_report = get_fire_events_report(
        valid_fire_events,
    )
    assert get_base_report_validation(fire_events_report)


def test_invalid_fire_events_chanel_value_check(
    valid_fire_events: FireEvents,
) -> None:
    valid_fire_events.add_timecode_chanel_duration(
        JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
        JSON_BINARY_PARAMETER.fire_chanel_value_bound.maximal + 1,
        0,
    )
    fire_events_report = get_fire_events_report(
        valid_fire_events,
    )
    if fire_events_report is None:
        msg = "Fire events report is None"
        raise ValueError(msg)
    assert len(fire_events_report.duration_chanel_infractions) == 1
    assert (
        fire_events_report.duration_chanel_infractions[0].dict()
        == IntegerBoundaryInfraction(
            data_type="fire chanel",
            event_index=3,
            value=3,
            value_min=0,
            value_max=2,
        ).dict()
    )


def test_invalid_fire_events_duration_value_check(
    valid_fire_events: FireEvents,
) -> None:
    valid_fire_events.add_timecode_chanel_duration(
        JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
        0,
        JSON_BINARY_PARAMETER.fire_duration_value_bound.maximal + 1,
    )
    fire_events_report = get_fire_events_report(
        valid_fire_events,
    )
    if fire_events_report is None:
        msg = "Fire events report is None"
        raise ValueError(msg)
    assert len(fire_events_report.duration_chanel_infractions) == 1
    assert (
        fire_events_report.duration_chanel_infractions[0].dict()
        == IntegerBoundaryInfraction(
            data_type="fire duration",
            event_index=3,
            value=256,
            value_min=0,
            value_max=255,
        ).dict()
    )
