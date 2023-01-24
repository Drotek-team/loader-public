from ....show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)
from .su_to_stc_procedure import su_to_stc_procedure


def test_su_to_stc_procedure():
    show_trajectory = su_to_stc_procedure(get_valid_show_user(ShowUserConfiguration()))
    assert show_trajectory.drone_number == 1
    assert len(show_trajectory.frames) == 1022
    assert show_trajectory.frames == list(range(1022))
    assert show_trajectory.drone_number == 1
