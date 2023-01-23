import numpy as np

from ....show_env.show_user.show_user_generator import (
    ShowUserConfiguration,
    get_valid_show_user,
)
from ...simulation.position_simulation import SimulationInfo
from .su_to_stc_procedure import (
    CollisionPositionInfo,
    get_position_info_from_simulation_infos,
    su_to_stc_procedure,
)


def test_get_position_info_from_simulation_infos():
    simulation_infos = [
        SimulationInfo(0, np.array([0.0, 0.0, 0.0]), in_air=False, in_dance=False),
        SimulationInfo(1, np.array([0.0, 0.0, 0.0]), in_air=False, in_dance=False),
        SimulationInfo(2, np.array([0.0, 0.0, 0.0]), in_air=False, in_dance=False),
    ]
    position_infos = get_position_info_from_simulation_infos(simulation_infos)
    assert position_infos == [
        CollisionPositionInfo(0, np.array([0.0, 0.0, 0.0]), in_air=False),
        CollisionPositionInfo(1, np.array([0.0, 0.0, 0.0]), in_air=False),
        CollisionPositionInfo(2, np.array([0.0, 0.0, 0.0]), in_air=False),
    ]


# TODO: get_valid_show_user
def test_su_to_stc_procedure():
    show_trajectory = su_to_stc_procedure(get_valid_show_user(ShowUserConfiguration()))
    assert show_trajectory.drone_number == 1
    assert len(show_trajectory.frames) == 1021
    assert show_trajectory.frames == list(range(1021))
    assert show_trajectory.drone_number == 1
