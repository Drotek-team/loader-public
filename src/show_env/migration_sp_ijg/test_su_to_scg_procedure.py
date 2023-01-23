import numpy as np
from hypothesis import given
from hypothesis import strategies as st

from src.show_env.iostar_json.show_configuration import ShowConfiguration

from ..show_user.show_user_generator import ShowUserConfiguration, get_valid_show_user
from .su_to_scg_procedure import su_to_sc_procedure


@given(
    nb_x=st.integers(1, 5),
    nb_y=st.integers(1, 5),
    nb_drone_per_family=st.integers(1, 5),
    step_takeoff=st.floats(1, 10),
    angle_takeoff=st.floats(0, 2 * np.pi),
    show_duration_absolute_time=st.floats(1.0, 10),
)
def test_su_to_sc_procedure_hypothesis(
    nb_x: int,
    nb_y: int,
    nb_drone_per_family: int,
    step_takeoff: float,
    angle_takeoff: float,
    show_duration_absolute_time: float,
):
    show_user_configuration = ShowUserConfiguration(
        nb_x=nb_x,
        nb_y=nb_y,
        nb_drone_per_family=nb_drone_per_family,
        step=step_takeoff,
        angle_takeoff=angle_takeoff,
        show_duration_absolute_time=show_duration_absolute_time,
    )
    show_user = get_valid_show_user(show_user_configuration)
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
    assert show_configuration == su_to_sc_procedure(
        get_valid_show_user(show_user_configuration)
    )
