from loader.show_env.migration_sp_ijg.su_to_ijg import su_to_ijg
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_iostar_json_gcs_standard_case_and_method() -> None:
    iostar_json_gcs = su_to_ijg(get_valid_show_user(ShowUserConfiguration()))
    assert iostar_json_gcs.nb_drones_per_family == 1
    iostar_json_gcs = su_to_ijg(
        get_valid_show_user(ShowUserConfiguration(nb_drone_per_family=3)),
    )
    assert iostar_json_gcs.nb_drones_per_family == 3
