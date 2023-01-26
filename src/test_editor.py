import json
import os
from pathlib import Path

from .editor import (
    apply_export_to_iostar_json,
    apply_export_to_iostar_json_gcs,
    create_empty_show_user,
    export_show_user_to_iostar_json_gcs_string,
    export_show_user_to_iostar_json_string,
    global_check_iostar_json_gcs,
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


def test_export_procedure_to_iostar_json_standard_case():
    _, show_check_report = apply_export_to_iostar_json(
        get_valid_show_user(
            ShowUserConfiguration(
                nb_x=1,
                nb_y=1,
                nb_drone_per_family=1,
                step=1.5,
                angle_takeoff=0,
                show_duration_absolute_time=30.0,
            )
        )
    )
    assert show_check_report.user_validation


def test_export_procedure_to_iostar_json_gcs_standard_case():
    _, show_check_report = apply_export_to_iostar_json_gcs(
        get_valid_show_user(
            ShowUserConfiguration(
                nb_x=1,
                nb_y=1,
                nb_drone_per_family=1,
                step=1.5,
                angle_takeoff=0,
                show_duration_absolute_time=30.0,
            )
        )
    )
    assert show_check_report.user_validation


def test_export_show_user_to_iostar_json_string_standard_case():
    iostar_json_string = export_show_user_to_iostar_json_string(
        get_valid_show_user(ShowUserConfiguration())
    )
    assert isinstance(iostar_json_string, str)


# WARNING: this test is fondamental as it is the only one which proves that the loader is compatible with px4 and the gcs
def test_export_show_user_to_iostar_json_gcs_string_standard_case():
    iostar_json_gcs_string = export_show_user_to_iostar_json_gcs_string(
        get_valid_show_user(ShowUserConfiguration(nb_x=2, nb_y=2, step=2.0))
    )
    with open(Path(os.getcwd()).joinpath("iostar_json_gcs_reference.json")) as f:
        assert json.loads(iostar_json_gcs_string) == json.load(f)


def test_global_check_iostar_json_standard_case():
    iostar_json_gcs = su_to_ijg(get_valid_show_user(ShowUserConfiguration()))
    assert global_check_iostar_json_gcs(iostar_json_gcs)
