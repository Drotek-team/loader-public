from ..show_user.show_user_generator import get_valid_show_user
from .export_procedure import apply_export_procedure

NB_X = 1
NB_Y = 1
NB_DRONE_PER_FAMILY = 1
STEP_TAKEOFF = 1.5
ANGLE_TAKEOFF = 0
SHOW_DURATION_FRAME = 1


def test_export_procedure():
    iostar_json, show_check_report = apply_export_procedure(
        get_valid_show_user(
            NB_X,
            NB_Y,
            NB_DRONE_PER_FAMILY,
            STEP_TAKEOFF,
            ANGLE_TAKEOFF,
            SHOW_DURATION_FRAME,
        )
    )
    assert show_check_report.validation
