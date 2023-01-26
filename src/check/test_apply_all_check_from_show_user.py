from ..show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)
from .all_check_from_show_user import apply_all_check_from_show_user


def test_apply_all_check_from_show_user_standard_case():
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    all_check_contenor = apply_all_check_from_show_user(valid_show_user)
    assert all_check_contenor.user_validation


def test_apply_all_check_from_show_user_incorrect_show_user_check():
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    valid_show_user[0].position_events[0].frame = 1
    all_check_contenor = apply_all_check_from_show_user(valid_show_user)
    assert not (all_check_contenor.user_validation)


def test_apply_all_check_from_show_user_incorrect_show_px4():
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    valid_show_user[0].add_position_event(-1, (0.0, 0.0, 0.0))
    all_check_contenor = apply_all_check_from_show_user(valid_show_user)
    assert not (all_check_contenor.user_validation)
    valid_show_user[0].add_position_event(-1, (0.0, 0.0, 0.0))
    all_check_contenor = apply_all_check_from_show_user(valid_show_user)
    assert not (all_check_contenor.user_validation)
