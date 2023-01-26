import numpy as np

from ....parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ....show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)
from .stc_to_ssc import stc_to_ss
from .su_to_stc import su_to_stc


def test_valid_show_flags():
    show_simulation = stc_to_ss(
        su_to_stc(
            get_valid_show_user(ShowUserConfiguration()),
        )
    )
    assert len(show_simulation.show_slices) == 1022
    assert np.array_equal(
        show_simulation.show_slices[0].in_air_positions[0],
        np.array([0.0, 0.0, 0.0]),
    )
    assert np.array_equal(
        show_simulation.show_slices[240].in_air_positions[0],
        np.array([0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min]),
    )
    assert len(show_simulation.show_slices[-1].in_air_positions) == 0
