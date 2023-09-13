import pytest
from loader.reports import BoundaryInfraction, IncreasingFrameInfraction
from loader.schemas.drone_px4.events import PositionEvents


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
    timecode_report = IncreasingFrameInfraction.generate(
        standard_position_events,
    )
    assert not len(timecode_report)


def test_get_timecode_report_bound_violation(
    standard_position_events: PositionEvents,
) -> None:
    standard_position_events.add_timecode_xyz(
        -1,
        (0, 0, 0),
    )
    standard_position_events.add_timecode_xyz(
        103079216,
        (0, 0, 0),
    )
    timecode_report = BoundaryInfraction.generate(
        standard_position_events,
    )
    assert len(timecode_report)
    assert timecode_report["timecode"][0] == BoundaryInfraction(
        event_index=3,
        value=-42,
    )
    assert timecode_report["timecode"][1] == BoundaryInfraction(
        event_index=4,
        value=4294967333,
    )


def test_get_timecode_report_increasing_frame_violation(
    standard_position_events: PositionEvents,
) -> None:
    standard_position_events.add_timecode_xyz(
        1,
        (0, 0, 0),
    )
    timecode_report = IncreasingFrameInfraction.generate(
        standard_position_events,
    )
    assert len(timecode_report)
    assert timecode_report[0] == IncreasingFrameInfraction(
        event_index=3,
        previous_frame=2,
        frame=1,
    )
