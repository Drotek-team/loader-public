import pytest

from .editor import (
    apply_export_procedure,
    create_show_user,
    export_show_user_to_iostar_json_gcs_string,
    export_show_user_to_iostar_json_string,
    global_check_iostar_json_gcs,
)
from .show_env.migration_sp_ijg.su_to_ijg_procedure import su_to_ijg_procedure
from .show_env.show_user.show_user import ShowUser
from .show_env.show_user.show_user_generator import get_valid_show_user

NB_X = 1
NB_Y = 1
NB_DRONE_PER_FAMILY = 1
STEP_TAKEOFF = 1.5
ANGLE_TAKEOFF = 0
SHOW_DURATION_SECOND = 30.0


def test_export_procedure():
    _, show_check_report = apply_export_procedure(
        get_valid_show_user(
            NB_X,
            NB_Y,
            NB_DRONE_PER_FAMILY,
            STEP_TAKEOFF,
            ANGLE_TAKEOFF,
            SHOW_DURATION_SECOND,
        )
    )
    assert show_check_report.user_validation


@pytest.fixture
def standard_show_user():
    show_user = create_show_user(1)
    show_user[0].add_position_event(0, (0.0, 0.0, 0.0))
    show_user[0].add_position_event(240, (0.0, 0.0, 1.0))
    return show_user


def test_create_show_user_standard_case():
    drone_number = 5
    show_user = create_show_user(drone_number)
    assert len(show_user) == drone_number
    for drone_index in range(drone_number):
        assert len(show_user[drone_index].position_events) == 0
        assert len(show_user[drone_index].color_events) == 0
        assert len(show_user[drone_index].fire_events) == 0


def test_export_show_user_to_iostar_json_string_standard_case(
    standard_show_user: ShowUser,
):
    iostar_json_string = export_show_user_to_iostar_json_string(standard_show_user)
    assert isinstance(iostar_json_string, str)


def test_export_show_user_to_iostar_json_gcs_string_standard_case(
    standard_show_user: ShowUser,
):
    iostar_json_gcs_string = export_show_user_to_iostar_json_gcs_string(
        standard_show_user
    )
    assert isinstance(iostar_json_gcs_string, str)


def test_global_check_iostar_json_standard_case(
    standard_show_user: ShowUser,
):
    iostar_json_gcs = su_to_ijg_procedure(standard_show_user)
    assert global_check_iostar_json_gcs(iostar_json_gcs)
