import pytest
from loader.check.simulation.land_simulation import land_simulation
from loader.check.simulation.position_simulation import (
    SimulationInfo,
    linear_interpolation,
)
from loader.parameter.iostar_dance_import_parameter.frame_parameter import (
    FRAME_PARAMETER,
)
from loader.parameter.iostar_flight_parameter.iostar_land_parameter import (
    LAND_PARAMETER,
)
from loader.show_env.show_user.show_user import PositionEventUser

NUMERICAL_TOLERANCE = 1e-3


@pytest.fixture
def valid_position_event_user_first_case() -> PositionEventUser:
    frame_start = 0
    position_x = 2.36
    position_y = 5.69
    return PositionEventUser(
        frame=frame_start,
        xyz=(
            position_x,
            position_y,
            LAND_PARAMETER.land_safe_hgt + NUMERICAL_TOLERANCE,
        ),
    )


@pytest.fixture
def valid_position_event_user_second_case() -> PositionEventUser:
    frame_start = 0
    position_x = 2.36
    position_y = 5.69
    return PositionEventUser(
        frame=frame_start,
        xyz=(
            position_x,
            position_y,
            LAND_PARAMETER.land_safe_hgt - NUMERICAL_TOLERANCE,
        ),
    )


def test_land_simulation_first_case(
    valid_position_event_user_first_case: PositionEventUser,
) -> None:
    real_land_simulation_infos = land_simulation(
        valid_position_event_user_first_case.xyz,
        valid_position_event_user_first_case.frame,
    )
    land_middle_position = (
        valid_position_event_user_first_case.xyz[0],
        valid_position_event_user_first_case.xyz[1],
        LAND_PARAMETER.get_second_land_altitude_start(
            valid_position_event_user_first_case.xyz[2],
        ),
    )
    land_end_position = (
        valid_position_event_user_first_case.xyz[0],
        valid_position_event_user_first_case.xyz[1],
        0,
    )
    theorical_position = linear_interpolation(
        land_middle_position,
        land_end_position,
        FRAME_PARAMETER.from_second_to_frame(
            LAND_PARAMETER.get_second_land_second_delta(
                valid_position_event_user_first_case.xyz[2],
            ),
        ),
    )
    theorical_land_simulation_infos = [
        SimulationInfo(
            frame=valid_position_event_user_first_case.frame + frame_index,
            position=theorical_position,
            in_air=True,
        )
        for frame_index, theorical_position in enumerate(theorical_position)
    ]
    assert len(real_land_simulation_infos) == len(theorical_land_simulation_infos)
    assert all(
        [
            real_land_simulation_info == theorical_land_simulation_info
            for real_land_simulation_info, theorical_land_simulation_info in zip(
                real_land_simulation_infos,
                theorical_land_simulation_infos,
            )
        ],
    )


def test_land_simulation_second_case(
    valid_position_event_user_second_case: PositionEventUser,
) -> None:
    real_land_simulation_infos = land_simulation(
        valid_position_event_user_second_case.xyz,
        valid_position_event_user_second_case.frame,
    )
    land_first_position = valid_position_event_user_second_case.xyz
    land_middle_position = (
        valid_position_event_user_second_case.xyz[0],
        valid_position_event_user_second_case.xyz[1],
        LAND_PARAMETER.get_second_land_altitude_start(
            valid_position_event_user_second_case.xyz[2],
        ),
    )
    land_end_position = (
        valid_position_event_user_second_case.xyz[0],
        valid_position_event_user_second_case.xyz[1],
        0,
    )

    first_theorical_position = linear_interpolation(
        land_first_position,
        land_middle_position,
        FRAME_PARAMETER.from_second_to_frame(
            LAND_PARAMETER.get_first_land_second_delta(land_first_position[2]),
        ),
    )
    second_theorical_position = linear_interpolation(
        land_middle_position,
        land_end_position,
        FRAME_PARAMETER.from_second_to_frame(
            LAND_PARAMETER.get_second_land_second_delta(land_middle_position[2]),
        ),
    )
    theorical_position = first_theorical_position + second_theorical_position
    theorical_land_simulation_infos = [
        SimulationInfo(
            frame=valid_position_event_user_second_case.frame + frame_index,
            position=theorical_position,
            in_air=True,
        )
        for frame_index, theorical_position in enumerate(theorical_position)
    ]
    assert len(real_land_simulation_infos) == len(theorical_land_simulation_infos)
    assert all(
        [
            real_land_simulation_info == theorical_land_simulation_info
            for real_land_simulation_info, theorical_land_simulation_info in zip(
                real_land_simulation_infos,
                theorical_land_simulation_infos,
            )
        ],
    )
