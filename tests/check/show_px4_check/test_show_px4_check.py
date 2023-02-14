from loader.check.show_px4_check.show_px4_check import apply_show_px4_report
from loader.report import get_base_report_validation
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_apply_show_px4_check_standard_case() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(nb_x=2, nb_y=2),
    )
    show_px4_report = apply_show_px4_report(valid_show_user)
    assert get_base_report_validation(show_px4_report)
    show_px4_report = apply_show_px4_report(valid_show_user)
    assert get_base_report_validation(show_px4_report)
