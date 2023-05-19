from math import radians

from loader.shows.migrations.su_to_ijg import (
    get_family_from_drones_px4,
    su_to_ijg,
)
from loader.shows.migrations.su_to_sp import su_to_sp
from loader.shows.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)


def test_get_family_from_drones_px4_standard_case() -> None:
    family_from_drone_px4 = get_family_from_drones_px4(
        su_to_sp(get_valid_show_user(ShowUserConfiguration(nb_x=2, step=2.0))),
    )
    assert len(family_from_drone_px4.drones) == 2
    assert family_from_drone_px4.x == 0
    assert family_from_drone_px4.y == -100
    assert family_from_drone_px4.z == 0


def test_sp_to_ijg_standard_case() -> None:
    iostar_json_gcs = su_to_ijg(
        get_valid_show_user(
            ShowUserConfiguration(
                nb_x=2,
                nb_y=2,
                step=2.0,
                angle_takeoff=radians(-113),
            ),
        ),
    )
    assert len(iostar_json_gcs.show.families) == 4
    assert iostar_json_gcs.show.angle_takeoff == 113
