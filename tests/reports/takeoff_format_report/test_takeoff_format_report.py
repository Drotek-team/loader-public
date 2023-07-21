from typing import Tuple

import pytest
from loader.parameters import TAKEOFF_PARAMETERS
from loader.reports import (
    DroneUserReport,
    MinimumPositionEventsInfraction,
    TakeoffFormatReport,
    TakeoffPositionInfraction,
)
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user


def test_takeoff_format_report_generate_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    takeoff_format_report_report = TakeoffFormatReport.generate(show_user)
    assert not len(takeoff_format_report_report)


def test_drone_user_report_generate_minimal_position_event_report() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())

    show_user.drones_user[0].position_events[1:] = []
    drone_user_report = DroneUserReport.generate(show_user.drones_user[0])
    assert drone_user_report == DroneUserReport(
        drone_index=0,
        minimal_position_event=MinimumPositionEventsInfraction(events_number=1),
    )

    show_user.drones_user[0].position_events = []
    drone_user_report = DroneUserReport.generate(show_user.drones_user[0])
    assert drone_user_report == DroneUserReport(
        drone_index=0,
        minimal_position_event=MinimumPositionEventsInfraction(events_number=0),
    )


@pytest.mark.parametrize(
    "first_position, second_position",
    [
        ((1, 0, 0), (0, 0, TAKEOFF_PARAMETERS.takeoff_altitude_meter_min)),
        ((0, 1, 0), (0, 0, TAKEOFF_PARAMETERS.takeoff_altitude_meter_min)),
        ((0, 0, 0), (1, 0, TAKEOFF_PARAMETERS.takeoff_altitude_meter_min)),
        ((0, 0, 0), (0, 1, TAKEOFF_PARAMETERS.takeoff_altitude_meter_min)),
    ],
)
def test_takeoff_position_infraction_generate_horizontal(
    first_position: Tuple[float, float, float],
    second_position: Tuple[float, float, float],
) -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())

    show_user.drones_user[0].position_events[0].xyz = first_position
    show_user.drones_user[0].position_events[1].xyz = second_position
    takeoff_position_infraction = TakeoffPositionInfraction.generate(
        show_user.drones_user[0],
    )
    assert takeoff_position_infraction == TakeoffPositionInfraction(
        start_position=first_position,
        end_position=second_position,
    )


@pytest.mark.parametrize(
    "altitude",
    [
        TAKEOFF_PARAMETERS.takeoff_altitude_meter_min - 1,
        TAKEOFF_PARAMETERS.takeoff_altitude_meter_max + 1,
    ],
)
def test_takeoff_position_infraction_generate_vertical(
    altitude: float,
) -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    show_user.drones_user[0].position_events[1].xyz = (0, 0, altitude)
    takeoff_position_infraction = TakeoffPositionInfraction.generate(
        show_user.drones_user[0],
    )
    assert takeoff_position_infraction == TakeoffPositionInfraction(
        start_position=(0, 0, 0),
        end_position=(0, 0, altitude),
    )
