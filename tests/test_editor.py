from pathlib import Path

from loader.check.collision_check.show_simulation_collision_check import su_to_ss
from loader.check.performance_check.performance_evaluation import Metric, MetricRange
from loader.editor import (
    IostarJsonGcs,
    convert_iostar_json_gcs_string_to_show_configuration_gcs,
    convert_iostar_json_gcs_string_to_show_user,
    convert_show_user_to_iostar_json_gcs,
    create_empty_show_user,
    get_collision_infractions,
    get_dance_size_infractions,
    get_drotek_check_from_iostar_json_gcs_string,
    get_drotek_check_from_show_user,
    get_drotek_check_summary_from_iostar_json_gcs_string,
    get_drotek_check_summary_from_show_user,
    get_performance_infractions,
    get_verified_iostar_json_gcs,
)
from loader.show_env.migration_sp_ijg.su_to_ijg import su_to_ijg
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_create_show_user_standard_case() -> None:
    drone_number = 5
    show_user = create_empty_show_user(drone_number)
    assert len(show_user) == drone_number
    for drone_index in range(drone_number):
        assert len(show_user[drone_index].position_events) == 0
        assert len(show_user[drone_index].color_events) == 0
        assert len(show_user[drone_index].fire_events) == 0


def test_get_performance_infractions() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    assert len(get_performance_infractions(show_user, {})) == 0
    assert (
        len(
            get_performance_infractions(
                show_user,
                {
                    Metric.VERTICAL_POSITION: MetricRange(
                        threshold=1.5,
                        standard_convention=False,
                    ),
                },
            ),
        )
        != 0
    )

    assert len(get_performance_infractions(show_user, {})) == 0


def test_get_collisions() -> None:
    show_simulation = su_to_ss(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2)),
    )
    assert get_collision_infractions(show_simulation) == []


def test_get_dance_size_report() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert len(get_dance_size_infractions(show_user)) == 0


def test_get_drotek_check_from_show_user_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert get_drotek_check_from_show_user(show_user).dict() == {
        "show_user": None,
        "show_px4": None,
        "performance": None,
        "collision": None,
    }


def test_get_drotek_check_summary_from_show_user_standard_case() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert get_drotek_check_summary_from_show_user(show_user).dict() == {
        "show_user": 0,
        "show_px4": 0,
        "performance": 0,
        "collision": 0,
    }


def test_global_check_iostar_json_gcs() -> None:
    iostar_json_gcs_string = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration()),
    ).json()
    assert get_drotek_check_from_iostar_json_gcs_string(
        iostar_json_gcs_string,
    ).dict() == {
        "show_user": None,
        "show_px4": None,
        "performance": None,
        "collision": None,
    }


def test_get_drotek_check_summary_from_iostar_json_gcs_string_standard_case() -> None:
    iostar_json_gcs_string = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2)),
    ).json()
    assert get_drotek_check_summary_from_iostar_json_gcs_string(
        iostar_json_gcs_string,
    ).dict() == {
        "show_user": 0,
        "show_px4": 0,
        "performance": 0,
        "collision": 0,
    }


def test_get_show_configuration_from_iostar_json_gcs_string() -> None:
    iostar_json_gcs_string = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=3)),
    ).json()
    assert convert_iostar_json_gcs_string_to_show_configuration_gcs(
        iostar_json_gcs_string,
    ).dict() == {
        "nb_x": 2,
        "nb_y": 3,
        "nb_drone_per_family": 1,
        "step": 100,
        "angle_takeoff": 0,
        "duration": 42541,
        "hull": [(100, -50), (0, -50), (-100, 50), (100, 50)],
        "altitude_range": (-100, 0),
    }


# WARNING: this test is fondamental as it is the only one which proves that the loader is compatible with px4 and the gcs
def test_export_show_user_to_iostar_json_gcs_string_standard_case() -> None:
    iostar_json_gcs_string = convert_show_user_to_iostar_json_gcs(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2, step=2.0)),
    )
    with (Path() / "iostar_json_gcs_reference.json").open() as f:
        assert iostar_json_gcs_string == IostarJsonGcs.parse_raw(f.read())


def test_import_iostar_json_gcs_string_to_show_user() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    iostar_json_gcs_string = su_to_ijg(show_user).json()
    assert (
        convert_iostar_json_gcs_string_to_show_user(iostar_json_gcs_string) == show_user
    )


def test_get_verified_iostar_json_gcs() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration())
    iostar_json_gcs = su_to_ijg(show_user)
    assert get_verified_iostar_json_gcs(iostar_json_gcs.json()) == iostar_json_gcs