from loader.check.collision_check.migration.su_to_sct import su_to_sct
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_su_to_sct() -> None:
    show_trajectory = su_to_sct(get_valid_show_user(ShowUserConfiguration()))
    assert show_trajectory.drone_number == 1
    assert len(show_trajectory.frames) == 1022
    assert show_trajectory.frames == list(range(1022))
    assert show_trajectory.drone_number == 1
