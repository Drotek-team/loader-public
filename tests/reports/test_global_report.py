from loader.reports import GlobalReport
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user


def test_global_report_summary_standard_case() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), show_duration_absolute_time=3),
    )
    global_report = GlobalReport.generate(valid_show_user)
    global_report_summary = global_report.summarize()
    assert global_report_summary.takeoff_format_summary is None
    assert global_report_summary.autopilot_format_summary is None
    assert global_report_summary.dance_size_summary is None
    assert global_report_summary.performance_summary is None
    assert global_report_summary.collision_summary is None
    assert not len(global_report_summary)


def test_global_report_summary_collision_report() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            matrix=get_matrix(nb_x=2, nb_y=2),
            step=0.3,
            show_duration_absolute_time=3,
        ),
    )
    global_report = GlobalReport.generate(valid_show_user)
    global_report_summary = global_report.summarize()
    assert global_report_summary.takeoff_format_summary is None
    assert global_report_summary.autopilot_format_summary is None
    assert global_report_summary.dance_size_summary is None
    assert global_report_summary.performance_summary is None
    assert global_report_summary.collision_summary is not None
    assert len(global_report_summary.collision_summary) == 2232
    assert len(global_report_summary)


def test_generate_global_report_standard_case() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    global_report = GlobalReport.generate(valid_show_user)
    assert not len(global_report)


def test_generate_global_report_takeoff_format_report_four_frame_tolerance() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), show_duration_absolute_time=3),
    )
    valid_show_user[0].position_events[0].frame = 4
    global_report = GlobalReport.generate(valid_show_user)
    assert not len(global_report)


def test_generate_global_report_incorrect_takeoff_format_report() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    valid_show_user[0].position_events[0].frame = 5
    global_report = GlobalReport.generate(valid_show_user)
    assert len(global_report)

    global_report = GlobalReport.generate(valid_show_user, without_takeoff_format=True)
    assert not len(global_report)


def test_generate_global_report_incorrect_autopilot_format() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    valid_show_user[0].add_position_event(-1, (0.0, 0.0, 0.0))
    global_report = GlobalReport.generate(valid_show_user)
    assert len(global_report)
    valid_show_user[0].add_position_event(-1, (0.0, 0.0, 0.0))
    global_report = GlobalReport.generate(valid_show_user)
    assert len(global_report)
