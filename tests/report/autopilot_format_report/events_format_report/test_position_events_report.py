import pytest
from loader.parameters import FRAME_PARAMETERS, TAKEOFF_PARAMETERS
from loader.parameters.json_binary_parameters import JSON_BINARY_PARAMETERS
from loader.reports import (
    CoordinateInfraction,
    PositionEventsReport,
)
from loader.schemas.drone_px4.events import PositionEvents


@pytest.fixture
def valid_position_events() -> PositionEvents:
    position_events = PositionEvents()
    position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETERS.show_start_frame,
        (0, 0, 0),
    )
    position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETERS.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETERS.show_start_frame
            + FRAME_PARAMETERS.from_second_to_frame(
                TAKEOFF_PARAMETERS.takeoff_duration_second,
            ),
        ),
        (
            0,
            0,
            -int(TAKEOFF_PARAMETERS.takeoff_altitude_meter_min),
        ),
    )
    return position_events


def test_valid_position_events_report(
    valid_position_events: PositionEvents,
) -> None:
    position_events_report = PositionEventsReport.generate(
        valid_position_events,
    )
    assert not len(position_events_report)


def test_invalid_position_events_xyz_value_report(
    valid_position_events: PositionEvents,
) -> None:
    valid_position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETERS.timecode_value_bound.maximal,
        (
            JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal + 1,
            JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal + 1,
            JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal + 1,
        ),
    )
    position_events_report = PositionEventsReport.generate(
        valid_position_events,
    )
    assert position_events_report is not None
    coordinate_infractions = position_events_report.coordinate_infractions
    assert len(coordinate_infractions) == 3
    for coordinate_infraction in coordinate_infractions:
        assert coordinate_infraction == CoordinateInfraction(
            event_index=2,
            value=JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal + 1,
            value_min=JSON_BINARY_PARAMETERS.coordinate_value_bound.minimal,
            value_max=JSON_BINARY_PARAMETERS.coordinate_value_bound.maximal,
        )
