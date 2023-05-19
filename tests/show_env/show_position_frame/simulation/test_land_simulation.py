import numpy as np
from hypothesis import example, given
from hypothesis import strategies as st
from loader.parameters import LAND_PARAMETERS
from loader.shows.show_position_frame.simulation.land_simulation import land_simulation
from loader.shows.show_position_frame.simulation.position_simulation import SimulationInfo

from tests.strategies import slow


@given(
    frame_start=st.integers(0, 100),
    x_position=st.floats(
        -10,
        10,
    ),
    y_position=st.floats(-10, 10),
)
@example(x_position=0, y_position=0.5625, frame_start=0)
@slow
def test_land_simulation_above_land_safe_hgt(
    frame_start: int,
    x_position: float,
    y_position: float,
) -> None:
    land_first_position = (x_position, y_position, LAND_PARAMETERS.land_safe_hgt + 3)
    land_middle_position = (
        x_position,
        y_position,
        LAND_PARAMETERS.land_safe_hgt,
    )
    land_end_position = (
        x_position,
        y_position,
        0,
    )
    real_land_simulation_infos = land_simulation(
        land_first_position,
        frame_start,
    )
    assert real_land_simulation_infos[0] == SimulationInfo(
        frame=frame_start,
        position=np.array(land_first_position),
        in_air=True,
    )
    assert real_land_simulation_infos[24] == SimulationInfo(
        frame=frame_start + 24,
        position=np.array(land_middle_position),
        in_air=True,
    )
    assert real_land_simulation_infos[-1].frame == frame_start + 203
    np.testing.assert_allclose(
        land_end_position,
        real_land_simulation_infos[-1].position,
        atol=1e-1,
    )
    assert real_land_simulation_infos[-1].in_air


@given(
    frame_start=st.integers(0, 100),
    x_position=st.floats(
        -10,
        10,
    ),
    y_position=st.floats(-10, 10),
)
@slow
def test_land_simulation_under_land_safe_hgt(
    frame_start: int,
    x_position: float,
    y_position: float,
) -> None:
    land_first_position = (x_position, y_position, LAND_PARAMETERS.land_safe_hgt - 1)
    land_end_position = (
        x_position,
        y_position,
        0,
    )
    real_land_simulation_infos = land_simulation(
        land_first_position,
        frame_start,
    )
    assert real_land_simulation_infos[0] == SimulationInfo(
        frame=frame_start,
        position=np.array(land_first_position),
        in_air=True,
    )
    assert real_land_simulation_infos[-1].frame == frame_start + 119
    np.testing.assert_allclose(
        land_end_position,
        real_land_simulation_infos[-1].position,
        atol=1e-1,
    )
    assert real_land_simulation_infos[-1].in_air


@given(
    frame_start=st.integers(0, 100),
    x_position=st.floats(
        -10,
        10,
    ),
    y_position=st.floats(-10, 10),
)
@slow
def test_land_simulation_in_land_safe_hgt(
    frame_start: int,
    x_position: float,
    y_position: float,
) -> None:
    land_first_position = (x_position, y_position, LAND_PARAMETERS.land_safe_hgt)
    land_end_position = (
        x_position,
        y_position,
        0,
    )
    real_land_simulation_infos = land_simulation(
        land_first_position,
        frame_start,
    )
    assert real_land_simulation_infos[0] == SimulationInfo(
        frame=frame_start,
        position=np.array(land_first_position),
        in_air=True,
    )
    assert real_land_simulation_infos[-1].frame == frame_start + 179
    np.testing.assert_allclose(
        land_end_position,
        real_land_simulation_infos[-1].position,
        atol=1e-1,
    )
    assert real_land_simulation_infos[-1].in_air
