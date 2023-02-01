import json
import os
from pathlib import Path

from src.check.performance_check.performance_evaluation import Metric, MetricRange

from .check.collision_check.show_simulation_collision_check import su_to_ss
from .editor import (
    create_empty_show_user,
    export_show_user_to_iostar_json_gcs_string,
    get_collisions,
    get_dance_size_report,
    get_performance_infractions,
    get_verified_iostar_json_gcs,
    global_check_iostar_json_gcs,
    global_check_show_user,
    import_iostar_json_gcs_string_to_show_user,
)
from .show_env.migration_sp_ijg.su_to_ijg import su_to_ijg
from .show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_create_show_user_standard_case():
    drone_number = 5
    show_user = create_empty_show_user(drone_number)
    assert len(show_user) == drone_number
    for drone_index in range(drone_number):
        assert len(show_user[drone_index].position_events) == 0
        assert len(show_user[drone_index].color_events) == 0
        assert len(show_user[drone_index].fire_events) == 0


def test_get_performance_infractions():
    show_user = get_valid_show_user(ShowUserConfiguration())
    assert get_performance_infractions(show_user, {}).user_validation
    assert not (
        get_performance_infractions(
            show_user,
            {
                Metric.VERTICAL_POSITION: MetricRange(
                    threshold=1.5, standard_convention=False
                )
            },
        ).user_validation
    )
    assert get_performance_infractions(show_user, {}).user_validation


def test_get_collisions():
    show_simulation = su_to_ss(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    )
    assert get_collisions(show_simulation).user_validation


def test_get_dance_size_report():
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert get_dance_size_report(show_user).user_validation


def test_global_check_show_user():
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2))
    assert global_check_show_user(show_user) == ""


def test_global_check_iostar_json_gcs():
    iostar_json_gcs_string = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration())
    ).json()
    assert global_check_iostar_json_gcs(iostar_json_gcs_string) == ""


# WARNING: this test is fondamental as it is the only one which proves that the loader is compatible with px4 and the gcs
def test_export_show_user_to_iostar_json_gcs_string_standard_case():
    iostar_json_gcs_string = export_show_user_to_iostar_json_gcs_string(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2, step=2.0))
    )
    with open(Path(os.getcwd()).joinpath("iostar_json_gcs_reference.json")) as f:
        assert json.loads(iostar_json_gcs_string) == json.load(f)


def test_import_iostar_json_gcs_string_to_show_user():
    show_user = get_valid_show_user(ShowUserConfiguration())
    iostar_json_gcs_string = su_to_ijg(show_user).json()
    assert (
        import_iostar_json_gcs_string_to_show_user(iostar_json_gcs_string) == show_user
    )


def test_get_verified_iostar_json_gcs():
    show_user = get_valid_show_user(ShowUserConfiguration())
    iostar_json_gcs = su_to_ijg(show_user)
    assert get_verified_iostar_json_gcs(iostar_json_gcs.json()) == iostar_json_gcs
