from pathlib import Path

import pytest
from loader import (
    IostarJsonGcs,
    ShowConfigurationGcs,
    ShowUser,
)
from loader.parameters import IostarPhysicParameters
from loader.report import (
    AutopilotFormatReport,
    CollisionReport,
    DanceSizeInformation,
    GlobalReport,
    GlobalReportSummary,
    PerformanceReport,
    get_dance_size_information,
)
from loader.shows.migration_sp_ijg.ijg_to_su import ijg_to_su
from loader.shows.migration_sp_ijg.su_to_ijg import su_to_ijg
from loader.shows.migration_sp_ijg.su_to_scg import su_to_scg
from loader.shows.migration_sp_su.su_to_sp import su_to_sp
from loader.shows.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user
from loader.shows.show_user.show_user import PositionEventUser


def test_create_show_user_standard_case() -> None:
    nb_drones = 5
    show_user = ShowUser.create(nb_drones)
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
        ShowUser.create(nb_drones)


def test_get_performance_infractions() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    show_user.drones_user[0].add_position_event(frame=1000, xyz=(0.0, 0.0, 0.0))
    assert PerformanceReport.generate(show_user) is None
    assert (
        PerformanceReport.generate(
            show_user,
            physic_parameters=IostarPhysicParameters(acceleration_max=0.0001),
        )
        is not None
    )
    assert PerformanceReport.generate(show_user) is None


def test_get_collisions() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert CollisionReport.generate(show_user) is None


def test_get_collisions_with_collision_distance_with_collisions() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    collision_report = CollisionReport.generate(
        show_user,
        physic_parameters=IostarPhysicParameters(security_distance_in_air=2),
    )
    assert collision_report is not None
    assert len(collision_report.collision_infractions) == 4080


def test_get_collisions_with_collision_distance_without_collision() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2, step=2))
    collision_report = CollisionReport.generate(
        show_user,
        physic_parameters=IostarPhysicParameters(security_distance_in_air=2),
    )
    assert collision_report is None


def test_get_collisions_with_collision_distance_inferior_to_minimal_distance() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    with pytest.raises(
        ValueError,
        match="collision_distance .* should be greater than or equal to security_distance_in_air .*",
    ):
        CollisionReport.generate(
            show_user,
            physic_parameters=IostarPhysicParameters(security_distance_in_air=0.5),
        )


def test_get_autopilot_format_report() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert AutopilotFormatReport.generate(show_user) is None


def test_get_dance_size_informations() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    show_px4 = su_to_sp(show_user)
    assert all(
        get_dance_size_information(drone_px4)
        == DanceSizeInformation(
            drone_index=drone_px4.index,
            dance_size=106,
            position_events_size_pct=0,
            color_events_size_pct=0,
            fire_events_size_pct=0,
        )
        for drone_px4 in show_px4
    )


def test_generate_report_from_show_user_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    global_report = GlobalReport.generate(show_user)
    assert global_report == GlobalReport(
        takeoff_format=None,
        autopilot_format=None,
        performance=None,
        collision=None,
    )
    assert global_report.summary() == GlobalReportSummary(
        takeoff_format=0,
        autopilot_format=0,
        performance=0,
        collision=0,
    )


def test_generate_report_from_show_user_with_collision() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    global_report = GlobalReport.generate(
        show_user,
        physic_parameters=IostarPhysicParameters(security_distance_in_air=2),
    )
    assert global_report.summary() == GlobalReportSummary(
        takeoff_format=0,
        autopilot_format=0,
        performance=0,
        collision=4080,
    )


def test_generate_report_from_show_user_with_performance() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    show_user.drones_user[0].add_position_event(
        frame=1000,
        xyz=(*show_user.drones_user[0].position_events[-1].xyz[0:2], 5.0),
    )
    global_report = GlobalReport.generate(
        show_user,
        physic_parameters=IostarPhysicParameters(velocity_up_max=2.0),
    )
    assert global_report.summary() == GlobalReportSummary(
        takeoff_format=0,
        autopilot_format=0,
        performance=1,
        collision=0,
    )
    global_report = GlobalReport.generate(show_user)
    assert global_report.summary() == GlobalReportSummary(
        takeoff_format=0,
        autopilot_format=0,
        performance=0,
        collision=0,
    )


def test_generate_report_from_show_user_without_takeoff_format() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    show_user.drones_user[0].position_events.insert(
        1,
        PositionEventUser(
            frame=100,
            xyz=show_user.drones_user[0].position_events[-1].xyz,
        ),
    )
    global_report = GlobalReport.generate(show_user)
    assert global_report.summary() == GlobalReportSummary(
        takeoff_format=1,
        autopilot_format=0,
        performance=0,
        collision=0,
    )
    global_report = GlobalReport.generate(show_user, without_takeoff_format=True)
    assert global_report.summary() == GlobalReportSummary(
        takeoff_format=0,
        autopilot_format=0,
        performance=0,
        collision=0,
    )


def test_generate_report_from_iostar_json_gcs_string() -> None:
    iostar_json_gcs = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration()),
    )
    show_user = ijg_to_su(iostar_json_gcs)
    global_report = GlobalReport.generate(show_user)
    assert global_report == GlobalReport(
        takeoff_format=None,
        autopilot_format=None,
        performance=None,
        collision=None,
    )
    assert global_report.summary() == GlobalReportSummary(
        takeoff_format=0,
        autopilot_format=0,
        performance=0,
        collision=0,
    )


def test_get_show_configuration_from_iostar_json_gcs_string() -> None:
    iostar_json_gcs = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=3)),
    )
    show_user = ijg_to_su(iostar_json_gcs)
    assert su_to_scg(show_user) == ShowConfigurationGcs(
        nb_x=2,
        nb_y=3,
        nb_drone_per_family=1,
        step=150,
        angle_takeoff=0,
        duration=42541,
        hull=[(-150, -75), (-150, 75), (150, 75), (150, -75)],
        altitude_range=(-100, 0),
    )


# WARNING: this test is fondamental as it is the only one which proves that the loader is compatible with px4 and the gcs
def test_convert_show_user_to_iostar_json_gcs_standard_case() -> None:
    iostar_json_gcs = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2, step=2.0)),
    )
    assert iostar_json_gcs == IostarJsonGcs.parse_file(Path() / "iostar_json_gcs_valid.json")


def test_convert_iostar_json_gcs_string_to_show_user() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    iostar_json_gcs_string = su_to_ijg(show_user).json()
    assert ijg_to_su(IostarJsonGcs.parse_raw(iostar_json_gcs_string)) == show_user


def test_get_verified_iostar_json_gcs() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    iostar_json_gcs_string = su_to_ijg(show_user).json()
    show_user = ijg_to_su(IostarJsonGcs.parse_raw(iostar_json_gcs_string))
    assert GlobalReport.generate(show_user).get_nb_errors() == 0


def test_get_verified_iostar_json_gcs_invalid() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(nb_x=2, nb_y=2, step=0.3, show_duration_absolute_time=3),
    )
    iostar_json_gcs_string = su_to_ijg(show_user).json()
    show_user = ijg_to_su(IostarJsonGcs.parse_raw(iostar_json_gcs_string))
    assert GlobalReport.generate(show_user).get_nb_errors() > 0
