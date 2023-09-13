import pytest
from loader.parameters import FRAME_PARAMETERS, TAKEOFF_PARAMETERS
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS, MagicNumber
from loader.reports import BoundaryInfraction, EventsReport
from loader.schemas.drone_px4.events import PositionEvents


@pytest.fixture
def valid_position_events(request: pytest.FixtureRequest) -> PositionEvents:
    position_events = PositionEvents(request.param)
    position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETERS.show_start_frame,
        (0, 0, 0),
    )
    position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETERS.show_start_frame
        + FRAME_PARAMETERS.from_second_to_frame(
            TAKEOFF_PARAMETERS.takeoff_duration_second,
        ),
        (
            0,
            0,
            -int(TAKEOFF_PARAMETERS.takeoff_altitude_meter_min),
        ),
    )
    return position_events


@pytest.mark.parametrize("valid_position_events", list(MagicNumber), indirect=True)
def test_valid_position_events_report(
    valid_position_events: PositionEvents,
) -> None:
    position_events_report = BoundaryInfraction.generate(
        valid_position_events,
    )
    assert not len(position_events_report)


@pytest.mark.parametrize("valid_position_events", list(MagicNumber), indirect=True)
def test_invalid_position_events_xyz_value_report(
    valid_position_events: PositionEvents,
) -> None:
    valid_position_events.add_timecode_xyz(
        1000,
        (
            JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal + 1,
            JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal + 1,
            JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal + 1,
        ),
    )
    position_events_report = EventsReport.generate(
        valid_position_events,
    )
    assert len(position_events_report)
    coordinate_infractions = position_events_report.boundary_infractions
    assert len(coordinate_infractions) == 3
    for (axis, coordinate_infraction), expected_axis in zip(
        coordinate_infractions.items(),
        ["north", "east", "down"],
    ):
        assert axis == expected_axis
        assert coordinate_infraction == [
            BoundaryInfraction(
                event_index=2,
                value=JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal + 1,
            ),
        ]
