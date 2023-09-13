from loader.reports import AutopilotFormatReport
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user


def test_generate_autopilot_format_report_standard_case() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)),
    )
    show_px4_report = AutopilotFormatReport.generate(valid_show_user)
    assert not len(show_px4_report)
    assert not len(show_px4_report.summarize())


def test_generate_autopilot_format_report_invalid_case() -> None:
    invalid_show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)),
    )
    invalid_show_user.drones_user[0].add_position_event(-1, (328.0, -328.0, 328.0))
    invalid_show_user.drones_user[1].add_position_event(-1, (328.0, -328.0, 328.0))
    invalid_show_user.drones_user[1].add_color_event(-2, (2.0, -1.0, -0.1, -1.1))
    invalid_show_user.drones_user[2].add_fire_event(-3, 4, 500)
    show_px4_report = AutopilotFormatReport.generate(invalid_show_user)
    assert len(show_px4_report) == len(show_px4_report.summarize()) == 20
    assert (
        show_px4_report.summarize().model_dump()["events_format_report_summary"]["drone_indices"]
        == "0-2"
    )
