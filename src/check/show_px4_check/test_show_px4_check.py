from ...show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)
from .show_px4_check import apply_show_px4_check


def test_apply_show_px4_check_standard_case():
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(nb_x=2, nb_y=2),
    )
    show_px4_check_contenor = apply_show_px4_check(valid_show_user)
    assert show_px4_check_contenor.user_validation
    show_px4_check_contenor = apply_show_px4_check(valid_show_user)
    assert show_px4_check_contenor.user_validation