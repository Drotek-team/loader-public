from typing import TYPE_CHECKING

import numpy as np
from hypothesis import given
from loader.schemas import IostarJsonGcs, ShowUser
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user
from loader.schemas.show_user.show_user import is_angles_equal

from tests.strategies import slow, st_angle_takeoff, st_matrix, st_step_takeoff

if TYPE_CHECKING:
    from numpy.typing import NDArray


@given(
    matrix=st_matrix(),
    step_takeoff=st_step_takeoff,
    angle_takeoff=st_angle_takeoff,
)
@slow
def test_ijg_to_su(
    matrix: "NDArray[np.intp]",
    step_takeoff: float,
    angle_takeoff: float,
) -> None:
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
    export_import_autopilot_format = ShowUser.from_iostar_json_gcs(iostar_json_gcs)
    assert is_angles_equal(
        export_import_autopilot_format.angle_takeoff,
        iostar_json_gcs_angle_takeoff_rad,
    )
    assert show_user == export_import_autopilot_format
