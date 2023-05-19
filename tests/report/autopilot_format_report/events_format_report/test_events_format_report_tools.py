import pytest
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.reports import (
    IncreasingFrameInfraction,
    IntegerBoundaryInfraction,
    TimecodeReport,
    get_report_validation,
)
from loader.shows.drone_px4.events import PositionEvents


@pytest.fixture
def standard_position_events() -> PositionEvents:
    position_events = PositionEvents()
    position_events.add_timecode_xyz(0, (0, 0, 0))
    position_events.add_timecode_xyz(1, (0, 0, 0))
    position_events.add_timecode_xyz(2, (0, 0, 0))
    return position_events


def test_get_timecode_report_standard_case(
    standard_position_events: PositionEvents,
) -> None:
    timecode_report = TimecodeReport.generate(
        standard_position_events,
    )
    assert get_report_validation(timecode_report)


def test_get_timecode_report_bound_violation(
    standard_position_events: PositionEvents,
) -> None:
    standard_position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETERS.timecode_value_bound.minimal - 1,
        (0, 0, 0),
    )
    standard_position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETERS.timecode_value_bound.maximal + 1,
        (0, 0, 0),
    )
    timecode_report = TimecodeReport.generate(
        standard_position_events,
    )
    assert timecode_report is not None
    assert timecode_report.bound_infractions[0] == IntegerBoundaryInfraction(
        event_index=3,
        value=JSON_BINARY_PARAMETERS.timecode_value_bound.minimal - 1,
        value_min=JSON_BINARY_PARAMETERS.timecode_value_bound.minimal,
        value_max=JSON_BINARY_PARAMETERS.timecode_value_bound.maximal,
    )
    assert timecode_report.bound_infractions[1] == IntegerBoundaryInfraction(
        event_index=4,
        value=JSON_BINARY_PARAMETERS.timecode_value_bound.maximal + 1,
        value_min=JSON_BINARY_PARAMETERS.timecode_value_bound.minimal,
        value_max=JSON_BINARY_PARAMETERS.timecode_value_bound.maximal,
    )


def test_get_timecode_report_increasing_frame_violation(
    standard_position_events: PositionEvents,
) -> None:
    standard_position_events.add_timecode_xyz(
        1,
        (0, 0, 0),
    )
    timecode_report = TimecodeReport.generate(
        standard_position_events,
    )
    assert timecode_report is not None
    assert timecode_report.increasing_infractions[0] == IncreasingFrameInfraction(
        event_index=3,
        previous_frame=2,
        frame=1,
    )
