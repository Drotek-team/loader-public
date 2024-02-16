import pytest
from loader.parameters import TAKEOFF_PARAMETERS
from loader.reports import (
    DroneUserReport,
    MinimumPositionEventsInfraction,
    TakeoffFormatReport,
    TakeoffPositionInfraction,
)
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user


def test_takeoff_format_report_generate_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    takeoff_format_report_report = TakeoffFormatReport.generate(show_user)
    assert len(takeoff_format_report_report) == len(takeoff_format_report_report.summarize()) == 0


def test_drone_user_report_generate_minimal_position_event_report() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=1)))

    show_user.drones_user[0].position_events[1:] = []  # pyright: ignore[reportUnknownArgumentType]
    show_user.drones_user[1].position_events[1:] = []  # pyright: ignore[reportUnknownArgumentType]
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

    takeoff_format_report = TakeoffFormatReport.generate(show_user)
    assert len(takeoff_format_report) == len(takeoff_format_report.summarize()) == 2


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
    first_position: tuple[float, float, float],
    second_position: tuple[float, float, float],
) -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=1)))

    show_user.drones_user[0].position_events[0].xyz = first_position
    show_user.drones_user[0].position_events[1].xyz = second_position
    show_user.drones_user[1].position_events[0].xyz = first_position
    show_user.drones_user[1].position_events[1].xyz = second_position
    takeoff_format_report = TakeoffFormatReport.generate(show_user)
    assert takeoff_format_report.drone_users[0].takeoff is not None
    assert takeoff_format_report.drone_users[
        0
    ].takeoff.position_infraction == TakeoffPositionInfraction(
        start_position=first_position,
        end_position=second_position,
    )
    assert len(takeoff_format_report) == len(takeoff_format_report.summarize()) == 2
    assert (
        takeoff_format_report.summarize().model_dump()["drone_user_report_summary"]["drone_indices"]
        == "0-1"
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
