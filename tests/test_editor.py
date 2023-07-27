from pathlib import Path

import numpy as np
import pytest
from loader.parameters import IostarPhysicParameters
from loader.reports import (
    AutopilotFormatReport,
    CollisionReport,
    DanceSizeReport,
    GlobalReport,
    PerformanceReport,
)
from loader.reports.dance_size_report import DanceSizeInfraction
from loader.schemas import IostarJsonGcs, PositionEventUser, ShowUser
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user

VALID_SHOW_CONFIGURATION = ShowUserConfiguration(
    matrix=get_matrix(matrix=[[1, 0, 1], [1, 1, 1]]),
    angle_takeoff=np.pi / 3,
    step=2.0,
)


def test_create_show_user_standard_case() -> None:
    nb_drones = 5
    show_user = ShowUser.create(nb_drones=nb_drones, angle_takeoff=0, step=1)
    assert len(show_user) == nb_drones
    for drone_index in range(nb_drones):
        assert len(show_user[drone_index].position_events) == 0
        assert len(show_user[drone_index].color_events) == 0
        assert len(show_user[drone_index].fire_events) == 0


@pytest.mark.parametrize("nb_drones", [0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10])
def test_create_show_user_invalid_nb_drones(nb_drones: int) -> None:
    with pytest.raises(
        ValueError,
        match=f"nb_drones must be positive, not {nb_drones}",
    ):
        ShowUser.create(nb_drones=nb_drones, angle_takeoff=0, step=1)


def test_get_performance_infractions() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    show_user.drones_user[0].add_position_event(frame=1000, xyz=(0.0, 0.0, 0.0))
    performance_report = PerformanceReport.generate(show_user)
    assert len(performance_report) == 0 == len(performance_report.summarize())
    performance_report = PerformanceReport.generate(
        show_user,
        physic_parameters=IostarPhysicParameters(acceleration_max=0.0001),
    )
    assert len(performance_report) == len(performance_report.summarize())
    performance_report = PerformanceReport.generate(show_user)
    assert len(performance_report) == 0 == len(performance_report.summarize())


def test_get_collisions() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    collision_report = CollisionReport.generate(show_user)
    assert len(collision_report) == 0 == len(collision_report.summarize())


def test_get_collisions_with_collision_distance_with_collisions() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    collision_report = CollisionReport.generate(
        show_user,
        physic_parameters=IostarPhysicParameters(minimum_distance=2),
    )
    assert len(collision_report) == 680 == len(collision_report.summarize())

    assert (
        collision_report.summarize().model_dump()["collision_infractions_summary"]["drone_indices"]
        == "0-3"
    )


def test_get_collisions_with_collision_distance_without_collision() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2), step=2),
    )
    collision_report = CollisionReport.generate(
        show_user,
        physic_parameters=IostarPhysicParameters(minimum_distance=2),
    )
    assert len(collision_report) == 0 == len(collision_report.summarize())


def test_get_collisions_with_collision_distance_inferior_to_minimum_distance() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    with pytest.raises(
        ValueError,
        match="collision_distance .* should be greater than or equal to minimum_distance .*",
    ):
        CollisionReport.generate(
            show_user,
            physic_parameters=IostarPhysicParameters(minimum_distance=0.5),
        )


def test_get_autopilot_format_report() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    autopilot_format_report = AutopilotFormatReport.generate(show_user)
    assert len(autopilot_format_report) == 0 == len(autopilot_format_report.summarize())


def test_get_dance_size_informations() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    dance_size_report = DanceSizeReport.generate(show_user)
    assert len(dance_size_report) == 0 == len(dance_size_report.summarize())
    for drone_user, dance_size_infraction in zip(
        show_user.drones_user,
        dance_size_report.dance_size_infractions,
    ):
        assert dance_size_infraction == DanceSizeInfraction(
            drone_index=drone_user.index,
            dance_size=106,
            position_percent=0.03,
            color_percent=0.02,
            fire_percent=0.02,
        )


def test_generate_report_from_show_user_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    global_report = GlobalReport.generate(show_user)
    assert global_report == GlobalReport(
        takeoff_format=None,
        autopilot_format=None,
        performance=None,
        collision=None,
    )
    global_report_summary = global_report.summarize()
    assert global_report_summary.takeoff_format_summary is None
    assert global_report_summary.autopilot_format_summary is None
    assert global_report_summary.dance_size_summary is None
    assert global_report_summary.performance_summary is None
    assert global_report_summary.collision_summary is None


def test_generate_report_from_show_user_with_collision() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    global_report = GlobalReport.generate(
        show_user,
        physic_parameters=IostarPhysicParameters(minimum_distance=2),
    )
    global_report_summary = global_report.summarize()
    assert global_report_summary.takeoff_format_summary is None
    assert global_report_summary.autopilot_format_summary is None
    assert global_report_summary.dance_size_summary is None
    assert global_report_summary.performance_summary is None
    assert global_report_summary.collision_summary is not None
    assert len(global_report_summary.collision_summary) == 680


def test_generate_report_from_show_user_with_performance() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    show_user.drones_user[0].add_position_event(
        frame=1000,
        xyz=(*show_user.drones_user[0].position_events[-1].xyz[0:2], 5.0),
    )
    global_report = GlobalReport.generate(
        show_user,
        physic_parameters=IostarPhysicParameters(velocity_up_max=2.0),
    )
    global_report_summary = global_report.summarize()
    assert global_report_summary.takeoff_format_summary is None
    assert global_report_summary.autopilot_format_summary is None
    assert global_report_summary.dance_size_summary is None
    assert global_report_summary.performance_summary is not None
    assert len(global_report_summary.performance_summary) == 1
    assert global_report_summary.collision_summary is None
    global_report = GlobalReport.generate(show_user)
    global_report_summary = global_report.summarize()
    assert global_report_summary.takeoff_format_summary is None
    assert global_report_summary.autopilot_format_summary is None
    assert global_report_summary.dance_size_summary is None
    assert global_report_summary.performance_summary is None
    assert global_report_summary.collision_summary is None


def test_generate_report_from_show_user_without_takeoff_format() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=2)))
    show_user.drones_user[0].position_events.insert(
        1,
        PositionEventUser(
            frame=100,
            xyz=show_user.drones_user[0].position_events[-1].xyz,
        ),
    )
    show_user.drones_user[1].position_events.insert(
        1,
        PositionEventUser(
            frame=100,
            xyz=show_user.drones_user[1].position_events[-1].xyz,
        ),
    )
    global_report = GlobalReport.generate(show_user)
    global_report_summary = global_report.summarize()
    assert global_report_summary.takeoff_format_summary is not None
    assert len(global_report_summary.takeoff_format_summary) == 2
    assert global_report_summary.autopilot_format_summary is None
    assert global_report_summary.dance_size_summary is None
    assert global_report_summary.performance_summary is None
    assert global_report_summary.collision_summary is None
    global_report = GlobalReport.generate(show_user, without_takeoff_format=True)
    global_report_summary = global_report.summarize()
    assert global_report_summary.takeoff_format_summary is None
    assert global_report_summary.autopilot_format_summary is None
    assert global_report_summary.dance_size_summary is None
    assert global_report_summary.performance_summary is None
    assert global_report_summary.collision_summary is None


def test_generate_report_from_iostar_json_gcs_string() -> None:
    iostar_json_gcs = IostarJsonGcs.from_show_user(
        get_valid_show_user(ShowUserConfiguration()),
    )
    show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
    global_report = GlobalReport.generate(show_user)
    assert global_report == GlobalReport(
        takeoff_format=None,
        autopilot_format=None,
        performance=None,
        collision=None,
    )
    global_report_summary = global_report.summarize()
    assert global_report_summary.takeoff_format_summary is None
    assert global_report_summary.autopilot_format_summary is None
    assert global_report_summary.dance_size_summary is None
    assert global_report_summary.performance_summary is None
    assert global_report_summary.collision_summary is None


def test_get_show_configuration_from_iostar_json_gcs_string() -> None:
    iostar_json_gcs = IostarJsonGcs.from_show_user(
        get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2, nb_y=3))),
    )
    show_user = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
    iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
    assert iostar_json_gcs.show.nb_x == 2
    assert iostar_json_gcs.show.nb_y == 3
    assert iostar_json_gcs.nb_drones_per_family == 1
    assert iostar_json_gcs.show.step == 150
    assert iostar_json_gcs.show.angle_takeoff == 0
    assert iostar_json_gcs.show.duration == 42542
    assert iostar_json_gcs.show.hull == [(-150, -75), (-150, 75), (150, 75), (150, -75)]
    assert iostar_json_gcs.show.altitude_range == (-100, 0)


# WARNING: this test is fondamental as it is the only one which proves that the loader is compatible with px4 and the gcs
def test_convert_show_user_to_iostar_json_gcs_standard_case() -> None:
    iostar_json_gcs = IostarJsonGcs.from_show_user(get_valid_show_user(VALID_SHOW_CONFIGURATION))
    assert iostar_json_gcs == IostarJsonGcs.model_validate_json(
        Path("iostar_json_gcs_valid.json").read_text(),
    )


def test_convert_iostar_json_gcs_string_to_show_user() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    iostar_json_gcs_string = IostarJsonGcs.from_show_user(show_user).model_dump_json()
    assert (
        ShowUser.from_iostar_json_gcs(IostarJsonGcs.model_validate_json(iostar_json_gcs_string))
        == show_user
    )


def test_get_verified_iostar_json_gcs() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    iostar_json_gcs_string = IostarJsonGcs.from_show_user(show_user).model_dump_json()
    show_user = ShowUser.from_iostar_json_gcs(
        IostarJsonGcs.model_validate_json(iostar_json_gcs_string),
    )
    global_report = GlobalReport.generate(show_user)
    assert len(global_report) == 0 == len(global_report.summarize())


def test_get_verified_iostar_json_gcs_invalid() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(
            matrix=get_matrix(nb_x=2, nb_y=2),
            step=0.3,
            show_duration_absolute_time=3,
        ),
    )
    iostar_json_gcs_string = IostarJsonGcs.from_show_user(show_user).model_dump_json()
    show_user = ShowUser.from_iostar_json_gcs(
        IostarJsonGcs.model_validate_json(iostar_json_gcs_string),
    )
    global_report = GlobalReport.generate(show_user)
    assert len(global_report) == len(global_report.summarize()) > 0
