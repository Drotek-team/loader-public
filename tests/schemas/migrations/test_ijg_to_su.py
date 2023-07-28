from typing import TYPE_CHECKING, Tuple

import numpy as np
from hypothesis import given
from loader.parameters import IOSTAR_PHYSIC_PARAMETERS_MAX, IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION
from loader.schemas import IostarJsonGcs, ShowUser
from loader.schemas.matrix import get_matrix
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user
from loader.schemas.show_user.show_user import is_angles_equal

from tests.strategies import slow, st_angle_takeoff, st_matrix_with_shape, st_step_takeoff

if TYPE_CHECKING:
    from numpy.typing import NDArray


@given(
    matrix_with_shape=st_matrix_with_shape(),
    step_takeoff=st_step_takeoff,
    angle_takeoff=st_angle_takeoff,
)
@slow
def test_ijg_to_su(
    matrix_with_shape: Tuple["NDArray[np.intp]", int, int, int],
    step_takeoff: float,
    angle_takeoff: float,
) -> None:
    matrix, nb_x, nb_y, nb_drones_per_family = matrix_with_shape
    show_user = get_valid_show_user(
        ShowUserConfiguration(
            matrix=matrix,
            step=step_takeoff,
            angle_takeoff=angle_takeoff,
        ),
    )
    iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
    iostar_json_gcs_angle_takeoff_rad = -np.deg2rad(iostar_json_gcs.show.angle_takeoff)
    assert is_angles_equal(show_user.angle_takeoff, iostar_json_gcs_angle_takeoff_rad)
    assert show_user.nb_x == iostar_json_gcs.show.nb_x
    assert show_user.nb_y == iostar_json_gcs.show.nb_y
    assert show_user.nb_drones_per_family == iostar_json_gcs.nb_drones_per_family

    export_import_autopilot_format = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
    assert is_angles_equal(
        export_import_autopilot_format.angle_takeoff,
        iostar_json_gcs_angle_takeoff_rad,
    )
    assert show_user.nb_x == export_import_autopilot_format.nb_x == nb_x
    assert show_user.nb_y == export_import_autopilot_format.nb_y == nb_y
    assert (
        show_user.nb_drones_per_family
        == export_import_autopilot_format.nb_drones_per_family
        == nb_drones_per_family
    )
    assert show_user == export_import_autopilot_format


def test_show_user_from_iostar_json_gcs_without_physic_parameters() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(
            matrix=get_matrix(),
            step=1,
            angle_takeoff=0,
        ),
    )
    iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
    iostar_json_gcs.physic_parameters = None
    show_user.from_iostar_json_gcs(iostar_json_gcs)
    assert show_user.physic_parameters == IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION


def test_show_user_from_iostar_json_gcs_with_physic_parameters() -> None:
    show_user = get_valid_show_user(
        ShowUserConfiguration(
            matrix=get_matrix(),
            step=1,
            angle_takeoff=0,
        ),
    )
    show_user.physic_parameters = IOSTAR_PHYSIC_PARAMETERS_MAX
    iostar_json_gcs = IostarJsonGcs.from_show_user(show_user)
    iostar_json_gcs.physic_parameters = None
    show_user.from_iostar_json_gcs(iostar_json_gcs)
    assert show_user.physic_parameters == IOSTAR_PHYSIC_PARAMETERS_MAX
