from loader.check.all_check_from_show_user import get_global_report
from loader.report import get_base_report_validation
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_global_report_summary_standard_case() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    global_report = get_global_report(valid_show_user)
    assert global_report.summary().show_user == 0
    assert global_report.summary().show_px4 == 0
    assert global_report.summary().performance == 0
    assert global_report.summary().collision == 0
    assert global_report.summary().is_valid()


def test_global_report_summary_collision_check() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(nb_x=2, nb_y=2, step=0.3),
    )
    global_report = get_global_report(valid_show_user)
    assert global_report.summary().show_user == 0
    assert global_report.summary().show_px4 == 0
    assert global_report.summary().performance == 0
    assert global_report.summary().collision == 6120
    assert not (global_report.summary().is_valid())


def test_apply_all_check_from_show_user_standard_case() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    global_report = get_global_report(valid_show_user)
    assert get_base_report_validation(global_report)


def test_apply_all_check_from_show_user_show_user_check_four_frame_tolerance() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    valid_show_user[0].position_events[0].frame = 4
    global_report = get_global_report(valid_show_user)
    assert get_base_report_validation(global_report)


def test_apply_all_check_from_show_user_incorrect_show_user_check() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    valid_show_user[0].position_events[0].frame = 5
    global_report = get_global_report(valid_show_user)
    assert not get_base_report_validation(global_report)


def test_apply_all_check_from_show_user_incorrect_show_px4() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    valid_show_user[0].add_position_event(-1, (0.0, 0.0, 0.0))
    global_report = get_global_report(valid_show_user)
    assert not get_base_report_validation(global_report)
    valid_show_user[0].add_position_event(-1, (0.0, 0.0, 0.0))
    global_report = get_global_report(valid_show_user)
    assert not get_base_report_validation(global_report)
