from loader.check.show_user_check import (
    get_show_user_report,
)
from loader.report import get_report_validation
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_apply_show_user_check_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    show_user_check_report = get_show_user_report(show_user)
    assert get_report_validation(show_user_check_report)
