from ..migration_sp_ijg.su_to_ijg_procedure import su_to_ijg_procedure
from ..show_user.show_user_generator import ShowUserConfiguration, get_valid_show_user


def test_iostar_json_gcs_standard_case_and_method():
    iostar_json_gcs = su_to_ijg_procedure(get_valid_show_user(ShowUserConfiguration()))
    assert iostar_json_gcs.nb_drones_per_family == 1
    iostar_json_gcs = su_to_ijg_procedure(
        get_valid_show_user(ShowUserConfiguration(nb_drone_per_family=3))
    )
    assert iostar_json_gcs.nb_drones_per_family == 3
