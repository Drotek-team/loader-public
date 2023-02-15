from loader.report.base import get_report_validation
from loader.report.takeoff_format_report import TakeoffFormatReport
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_apply_takeoff_format_report_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    takeoff_format_report_report = TakeoffFormatReport.generate(show_user)
    assert get_report_validation(takeoff_format_report_report)
