from loader.schemas import IostarJsonGcs
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user


def test_iostar_json_gcs_standard_case_and_method() -> None:
    iostar_json_gcs = IostarJsonGcs.from_show_user(get_valid_show_user(ShowUserConfiguration()))
    assert iostar_json_gcs.nb_drones_per_family == 1
    iostar_json_gcs = IostarJsonGcs.from_show_user(
        get_valid_show_user(ShowUserConfiguration(get_matrix(nb_drones_per_family=3))),
    )
    assert iostar_json_gcs.nb_drones_per_family == 3
