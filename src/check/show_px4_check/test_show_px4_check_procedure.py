from ...show_env.show_user.show_user_generator import get_valid_show_user
from .show_px4_check_procedure import apply_show_px4_check_procedure


def test_apply_show_px4_check_procedure_standard_case():
    valid_show_user = get_valid_show_user(
        nb_x=2,
        nb_y=2,
    )
    show_px4_check_contenor = apply_show_px4_check_procedure(valid_show_user)
    assert show_px4_check_contenor.user_validation
