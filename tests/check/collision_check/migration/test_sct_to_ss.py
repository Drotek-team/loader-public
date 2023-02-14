import numpy as np
from loader.check.collision_check.migration.sct_to_ss import sct_to_ss
from loader.check.collision_check.migration.su_to_sct import su_to_sct
from loader.parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_valid_show_flags() -> None:
    show_simulation = sct_to_ss(
        su_to_sct(
            get_valid_show_user(ShowUserConfiguration(nb_x=2)),
        ),
    )
    assert len(show_simulation.show_slices) == 1022
    assert np.array_equal(
        show_simulation.show_slices[0].in_air_positions[0],
        np.array([-0.5, 0.0, 0.0], dtype=np.float64),
    )
    assert np.array_equal(
        show_simulation.show_slices[240].in_air_positions[0],
        np.array(
            [-0.5, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min],
            dtype=np.float64,
        ),
    )
    assert len(show_simulation.show_slices[-1].in_air_positions) == 0
