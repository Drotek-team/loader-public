from loader.report.autopilot_format_report import AutopilotFormatReport
from loader.report.base import get_report_validation
from loader.shows.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_generate_autopilot_format_report_standard_case() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(nb_x=2, nb_y=2),
    )
    show_px4_report = AutopilotFormatReport.generate(valid_show_user)
    assert get_report_validation(show_px4_report)
