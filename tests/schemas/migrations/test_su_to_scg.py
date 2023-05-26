from hypothesis import given
from hypothesis import strategies as st
from loader.schemas.grid_configuration import GridConfiguration
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user

from tests.strategies import (
    slow,
    st_angle_takeoff,
    st_nb_drone_per_family,
    st_nb_x,
    st_nb_y,
    st_step_takeoff,
)


@given(
    nb_x=st_nb_x,
    nb_y=st_nb_y,
    nb_drone_per_family=st_nb_drone_per_family,
    step_takeoff=st_step_takeoff,
    angle_takeoff=st_angle_takeoff,
    show_duration_absolute_time=st.floats(1.0, 10),
)
@slow
def test_su_to_sc_hypothesis(
    nb_x: int,
    nb_y: int,
    nb_drone_per_family: int,
    step_takeoff: float,
    angle_takeoff: float,
    show_duration_absolute_time: float,
) -> None:
    show_user_configuration = ShowUserConfiguration(
        matrix=get_matrix(nb_x=nb_x, nb_y=nb_y, nb_drone_per_family=nb_drone_per_family),
        step=step_takeoff,
        angle_takeoff=angle_takeoff,
        show_duration_absolute_time=show_duration_absolute_time,
    )
    show_user = get_valid_show_user(show_user_configuration)
    position = (100.0, 100.0, 100.0)
    show_user.drones_user[0].add_position_event(10000, position)
    show_configuration = GridConfiguration(
        matrix=get_matrix(nb_x=nb_x, nb_y=nb_y, nb_drone_per_family=nb_drone_per_family),
        step=step_takeoff,
        angle_takeoff=angle_takeoff,
        duration=show_user.duration,
        hull=show_user.convex_hull,
        altitude_range=show_user.altitude_range,
    )
    assert position[:2] in show_configuration.hull
    assert show_configuration == GridConfiguration.from_show_user(show_user)
