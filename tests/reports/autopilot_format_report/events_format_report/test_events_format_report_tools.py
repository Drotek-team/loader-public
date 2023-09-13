import pytest
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, MagicNumber
from loader.reports import BoundaryInfraction, IncreasingFrameInfraction
from loader.schemas.drone_px4.events import PositionEvents


@pytest.fixture
def standard_position_events(request: pytest.FixtureRequest) -> PositionEvents:
    position_events = PositionEvents(request.param)
    position_events.add_timecode_xyz(0, (0, 0, 0))
    position_events.add_timecode_xyz(1, (0, 0, 0))
    position_events.add_timecode_xyz(2, (0, 0, 0))
    return position_events


@pytest.mark.parametrize("standard_position_events", list(MagicNumber), indirect=True)
def test_get_timecode_report_standard_case(
    standard_position_events: PositionEvents,
) -> None:
    timecode_report = IncreasingFrameInfraction.generate(
        standard_position_events,
    )
    assert not len(timecode_report)


@pytest.mark.parametrize(
    "standard_position_events, min_frame, max_frame, min_time, max_time",
    zip(
        list(MagicNumber),
        [
            JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(
                JSON_BINARY_PARAMETERS.time_value_bound(MagicNumber.old).minimal,
            )
            - 1,
            JSON_BINARY_PARAMETERS.time_value_bound(MagicNumber.new).minimal - 1,
        ],
        [
            JSON_BINARY_PARAMETERS.from_px4_timecode_to_user_frame(
                JSON_BINARY_PARAMETERS.time_value_bound(MagicNumber.old).maximal,
            )
            + 1,
            JSON_BINARY_PARAMETERS.time_value_bound(MagicNumber.new).maximal + 1,
        ],
        [
            -42,
            -1,
        ],
        [
            4294967333,
            65536,
        ],
    ),
    indirect=["standard_position_events"],
)
def test_get_timecode_report_bound_violation(
    standard_position_events: PositionEvents,
    min_frame: int,
    max_frame: int,
    min_time: int,
    max_time: int,
) -> None:
    standard_position_events.add_timecode_xyz(min_frame, (0, 0, 0))
    standard_position_events.add_timecode_xyz(max_frame, (0, 0, 0))
    timecode_report = BoundaryInfraction.generate(
        standard_position_events,
    )
    assert len(timecode_report) == 1
    assert timecode_report["time"][0] == BoundaryInfraction(
        event_index=3,
        value=min_time,
    )
    assert timecode_report["time"][1] == BoundaryInfraction(
        event_index=4,
        value=max_time,
    )


@pytest.mark.parametrize("standard_position_events", list(MagicNumber), indirect=True)
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
