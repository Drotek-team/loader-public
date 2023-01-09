import pytest

from ....parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ....parameter.iostar_flight_parameter.iostar_land_parameter import LAND_PARAMETER
from ....show_user.show_user import PositionEventUser
from ...simulation.land_simulation import land_simulation
from ..in_air_flight_simulation import linear_interpolation
from ..position_simulation import SimulationInfo

NUMERICAL_TOLERANCE = 1e-3


@pytest.fixture
def valid_position_event_user_first_case() -> PositionEventUser:
    FRAME_START = 0
    POSITION_X = 2.36
    POSITION_Y = 5.69
    return PositionEventUser(
        frame=FRAME_START,
        xyz=(
            POSITION_X,
            POSITION_Y,
            LAND_PARAMETER.land_safe_hgt + NUMERICAL_TOLERANCE,
        ),
    )


@pytest.fixture
def valid_position_event_user_second_case() -> PositionEventUser:

    FRAME_START = 0
    POSITION_X = 2.36
    POSITION_Y = 5.69
    return PositionEventUser(
        frame=FRAME_START,
        xyz=(
            POSITION_X,
            POSITION_Y,
            LAND_PARAMETER.land_safe_hgt - NUMERICAL_TOLERANCE,
        ),
    )


def test_land_simulation_first_case(
    valid_position_event_user_first_case: PositionEventUser,
):

    real_land_simulation_infos = land_simulation(
        valid_position_event_user_first_case.xyz,
        valid_position_event_user_first_case.position_frame,
    )
    land_middle_position = (
        valid_position_event_user_first_case.xyz[0],
        valid_position_event_user_first_case.xyz[1],
        LAND_PARAMETER.get_second_land_altitude_start(
            valid_position_event_user_first_case.xyz[2]
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
        int(
            LAND_PARAMETER.get_second_land_second_delta(
                valid_position_event_user_first_case.xyz[2]
            )
            * FRAME_PARAMETER.position_fps
        ),
    )
    theorical_land_simulation_infos = [
        SimulationInfo(
            valid_position_event_user_first_case.position_frame + frame_index,
            theorical_position,
            True,
            False,
        )
        for frame_index, theorical_position in enumerate(theorical_position)
    ]
    assert len(real_land_simulation_infos) == len(theorical_land_simulation_infos)
    assert all(
        [
            real_land_simulation_info == theorical_land_simulation_info
            for real_land_simulation_info, theorical_land_simulation_info in zip(
                real_land_simulation_infos, theorical_land_simulation_infos
            )
        ]
    )


def test_land_simulation_second_case(
    valid_position_event_user_second_case: PositionEventUser,
):

    real_land_simulation_infos = land_simulation(
        valid_position_event_user_second_case.xyz,
        valid_position_event_user_second_case.position_frame,
    )
    land_first_position = valid_position_event_user_second_case.xyz
    land_middle_position = (
        valid_position_event_user_second_case.xyz[0],
        valid_position_event_user_second_case.xyz[1],
        LAND_PARAMETER.get_second_land_altitude_start(
            valid_position_event_user_second_case.xyz[2]
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
        int(
            LAND_PARAMETER.get_first_land_second_delta(land_first_position[2])
            * FRAME_PARAMETER.position_fps
        ),
    )
    second_theorical_position = linear_interpolation(
        land_middle_position,
        land_end_position,
        int(
            LAND_PARAMETER.get_second_land_second_delta(land_middle_position[2])
            * FRAME_PARAMETER.position_fps
        ),
    )
    theorical_position = first_theorical_position + second_theorical_position
    theorical_land_simulation_infos = [
        SimulationInfo(
            valid_position_event_user_second_case.position_frame + frame_index,
            theorical_position,
            True,
            False,
        )
        for frame_index, theorical_position in enumerate(theorical_position)
    ]
    assert len(real_land_simulation_infos) == len(theorical_land_simulation_infos)
    assert all(
        [
            real_land_simulation_info == theorical_land_simulation_info
            for real_land_simulation_info, theorical_land_simulation_info in zip(
                real_land_simulation_infos, theorical_land_simulation_infos
            )
        ]
    )
