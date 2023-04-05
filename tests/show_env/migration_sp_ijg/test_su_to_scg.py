from hypothesis import given
from hypothesis import strategies as st
from loader.show_env.iostar_json.show_configuration import ShowConfiguration
from loader.show_env.migration_sp_ijg.su_to_scg import su_to_sc
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)

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
        nb_x=nb_x,
        nb_y=nb_y,
        nb_drone_per_family=nb_drone_per_family,
        step=step_takeoff,
        angle_takeoff=angle_takeoff,
        show_duration_absolute_time=show_duration_absolute_time,
    )
    show_user = get_valid_show_user(show_user_configuration)
    position = (100.0, 100.0, 100.0)
    show_user.drones_user[0].add_position_event(10000, position)
    show_configuration = ShowConfiguration(
        nb_x=nb_x,
        nb_y=nb_y,
        nb_drone_per_family=nb_drone_per_family,
        step=step_takeoff,
        angle_takeoff=angle_takeoff,
        duration=show_user.duration,
        hull=show_user.convex_hull,
        altitude_range=show_user.altitude_range,
    )
    assert position[:2] in show_configuration.hull
    assert show_configuration == su_to_sc(show_user)
