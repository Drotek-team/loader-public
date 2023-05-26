import numpy as np
from loader.schemas import IostarJsonGcs, ShowUser
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user


def test_ijg_to_su() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(matrix=get_matrix(nb_x=2), step=2.0, angle_takeoff=np.pi / 2),
    )
    iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
    iostar_json_gcs_angle_takeoff_rad = -np.deg2rad(iostar_json_gcs.show.angle_takeoff)
    assert show_user.angle_takeoff == iostar_json_gcs_angle_takeoff_rad
    export_import_autopilot_format = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
    assert export_import_autopilot_format.angle_takeoff == iostar_json_gcs_angle_takeoff_rad
    assert show_user == export_import_autopilot_format
