from loader.report.base import get_report_validation
from loader.report.global_report import GlobalReport
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_global_report_summary_standard_case() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(nb_x=2, nb_y=2, show_duration_absolute_time=3),
    )
    global_report = GlobalReport.generate(valid_show_user)
    assert global_report.summary().takeoff_format == 0
    assert global_report.summary().autopilot_format == 0
    assert global_report.summary().performance == 0
    assert global_report.summary().collision == 0
    assert global_report.summary().is_valid()


def test_global_report_summary_collision_report() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(nb_x=2, nb_y=2, step=0.3, show_duration_absolute_time=3),
    )
    global_report = GlobalReport.generate(valid_show_user)
    assert global_report.summary().takeoff_format == 0
    assert global_report.summary().autopilot_format == 0
    assert global_report.summary().performance == 0
    assert global_report.summary().collision == 2232
    assert not global_report.summary().is_valid()


def test_generate_global_report_standard_case() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    global_report = GlobalReport.generate(valid_show_user)
    assert get_report_validation(global_report)


def test_generate_global_report_takeoff_format_report_four_frame_tolerance() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(nb_x=2, nb_y=2, show_duration_absolute_time=3),
    )
    valid_show_user[0].position_events[0].frame = 4
    global_report = GlobalReport.generate(valid_show_user)
    assert get_report_validation(global_report)


def test_generate_global_report_incorrect_takeoff_format_report() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    valid_show_user[0].position_events[0].frame = 5
    global_report = GlobalReport.generate(valid_show_user)
    assert not get_report_validation(global_report)

    global_report = GlobalReport.generate(valid_show_user, without_takeoff_format=True)
    assert get_report_validation(global_report)


def test_generate_global_report_incorrect_autopilot_format() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    valid_show_user[0].add_position_event(-1, (0.0, 0.0, 0.0))
    global_report = GlobalReport.generate(valid_show_user)
    assert not get_report_validation(global_report)
    valid_show_user[0].add_position_event(-1, (0.0, 0.0, 0.0))
    global_report = GlobalReport.generate(valid_show_user)
    assert not get_report_validation(global_report)
