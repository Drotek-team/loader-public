from ..migration_sp_su.su_to_sp_procedure import su_to_sp_procedure
from ..show_user.show_user_generator import ShowUserConfiguration, get_valid_show_user
from .su_to_ijg_procedure import get_family_from_drones_px4, su_to_ijg_procedure


def test_get_family_from_drones_px4_standard_case():
    family_from_drone_px4 = get_family_from_drones_px4(
        su_to_sp_procedure(
            get_valid_show_user(ShowUserConfiguration(nb_y=2, step_takeoff=2.0))
        )
    )
    assert len(family_from_drone_px4.drones) == 2
    assert family_from_drone_px4.x == -100
    assert family_from_drone_px4.y == 0
    assert family_from_drone_px4.z == 0


def test_sp_to_ijg_procedure_standard_case():
    iostar_json_gcs = su_to_ijg_procedure(
        get_valid_show_user(ShowUserConfiguration(nb_y=2, step_takeoff=2.0))
    )
    assert len(iostar_json_gcs.show.families) == 2
