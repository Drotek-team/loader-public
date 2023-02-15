import pytest
from loader.parameter.iostar_dance_import_parameter.frame_parameter import (
    FRAME_PARAMETER,
)
from loader.parameter.iostar_dance_import_parameter.json_binary_parameter import (
    JSON_BINARY_PARAMETER,
)
from loader.parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from loader.report.autopilot_format_report.events_format_report import (
    CoordinateInfraction,
    PositionEventsReport,
)
from loader.report.base import get_report_validation
from loader.show_env.autopilot_format.drone_px4.events import PositionEvents


@pytest.fixture
def valid_position_events() -> PositionEvents:
    position_events = PositionEvents()
    position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETER.show_start_frame,
        (0, 0, 0),
    )
    position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETER.from_user_frame_to_px4_timecode(
            JSON_BINARY_PARAMETER.show_start_frame
            + FRAME_PARAMETER.from_second_to_frame(
                TAKEOFF_PARAMETER.takeoff_duration_second,
            ),
        ),
        (
            0,
            0,
            -int(TAKEOFF_PARAMETER.takeoff_altitude_meter_min),
        ),
    )
    return position_events


def test_valid_position_events_report(
    valid_position_events: PositionEvents,
) -> None:
    position_events_report = PositionEventsReport.generate(
        valid_position_events,
    )
    assert get_report_validation(position_events_report)


def test_invalid_position_events_xyz_value_report(
    valid_position_events: PositionEvents,
) -> None:
    valid_position_events.add_timecode_xyz(
        JSON_BINARY_PARAMETER.timecode_value_bound.maximal,
        (
            JSON_BINARY_PARAMETER.coordinate_value_bound.maximal + 1,
            JSON_BINARY_PARAMETER.coordinate_value_bound.maximal + 1,
            JSON_BINARY_PARAMETER.coordinate_value_bound.maximal + 1,
        ),
    )
    position_events_report = PositionEventsReport.generate(
        valid_position_events,
    )
    if position_events_report is None:
        msg = "Position events report is None"
        raise ValueError(msg)
    coordinate_infractions = position_events_report.coordinate_infractions
    assert len(coordinate_infractions) == 3
    for coordinate_infraction in coordinate_infractions:
        assert (
            coordinate_infraction.dict()
            == CoordinateInfraction(
                event_index=2,
                value=JSON_BINARY_PARAMETER.coordinate_value_bound.maximal + 1,
                value_min=JSON_BINARY_PARAMETER.coordinate_value_bound.minimal,
                value_max=JSON_BINARY_PARAMETER.coordinate_value_bound.maximal,
            ).dict()
        )
