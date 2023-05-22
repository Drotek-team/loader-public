from loader.shows import IostarJsonGcs, ShowUser
from loader.shows.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_ijg_to_su() -> None:
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, step=2.0))
    export_import_autopilot_format = ShowUser.from_iostar_json_gcs(
        IostarJsonGcs.from_show_user(show_user),
    )
    assert show_user == export_import_autopilot_format
