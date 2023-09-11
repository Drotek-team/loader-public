from math import radians

from loader.schemas import IostarJsonGcs
from loader.schemas.drone_px4 import DronePx4
from loader.schemas.iostar_json_gcs.iostar_json_gcs import Family
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user


def test_get_family_from_drones_px4_standard_case() -> None:
    family_from_drone_px4 = Family.from_drone_px4(
        DronePx4.from_show_user(
            get_valid_show_user(ShowUserConfiguration(matrix=get_matrix(nb_x=2), step=2.0)),
        )[:1],
    )
    assert len(family_from_drone_px4.drones) == 1
    assert family_from_drone_px4.x == 0
    assert family_from_drone_px4.y == -100
    assert family_from_drone_px4.z == 0


def test_sp_to_ijg_standard_case() -> None:
    iostar_json_gcs = IostarJsonGcs.from_show_user(
        get_valid_show_user(
            ShowUserConfiguration(
                matrix=get_matrix(nb_x=2, nb_y=2),
                step=2.0,
                angle_takeoff=radians(-113),
            ),
        ),
    )
    assert len(iostar_json_gcs.show.families) == 4
    assert iostar_json_gcs.show.angle_takeoff == 113
