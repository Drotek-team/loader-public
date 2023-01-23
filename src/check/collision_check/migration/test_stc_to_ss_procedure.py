import numpy as np

from ....parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ....show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)
from .stc_to_ssc_procedure import stc_to_ss_procedure
from .su_to_stc_procedure import su_to_stc_procedure


def test_valid_show_flags():
    show_simulation = stc_to_ss_procedure(
        su_to_stc_procedure(
            get_valid_show_user(ShowUserConfiguration()),
        )
    )
    assert len(show_simulation.show_slices) == 1021
    assert np.array_equal(
        show_simulation.show_slices[0].positions[0], np.array([0.0, 0.0, 0.0])
    )
    assert np.array_equal(show_simulation.show_slices[0].in_air_flags, np.array([True]))
    assert np.array_equal(
        show_simulation.show_slices[240].positions[0],
        np.array([0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min]),
    )

    assert np.array_equal(
        show_simulation.show_slices[-1].positions[0],
        np.array([0.0, 0.0, 0.0]),
    )
    assert np.array_equal(
        show_simulation.show_slices[-1].in_air_flags, np.array([False])
    )
