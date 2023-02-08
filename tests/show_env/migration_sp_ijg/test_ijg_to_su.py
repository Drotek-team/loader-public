from loader.show_env.migration_sp_ijg.ijg_to_su import ijg_to_su
from loader.show_env.migration_sp_ijg.su_to_ijg import su_to_ijg
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_ijg_to_su() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, step=2.0))
    export_import_show_px4 = ijg_to_su(su_to_ijg(show_user))
    assert show_user == export_import_show_px4
