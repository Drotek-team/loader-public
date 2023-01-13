import pytest

from .editor import (
    create_show_user,
    export_show_user_to_iostar_json_gcs_string,
    export_show_user_to_iostar_json_string,
    global_check_iostar_json_gcs,
)
from .migration.migration_sp_ijg.sp_to_ijg_procedure import sp_to_ijg_procedure
from .migration.migration_sp_su.su_to_sp_procedure import su_to_sp_procedure
from .migration.show_user.show_user import ShowUser


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


def test_create_show_incorrect_input():
    not_integer_input = "popo"
    inferior_to_one_input = 0
    with pytest.raises(TypeError, match=f"{not_integer_input} is not an integer"):
        create_show_user(not_integer_input)
    with pytest.raises(
        ValueError, match=f"{inferior_to_one_input} is not a positive integer"
    ):
        create_show_user(inferior_to_one_input)


def test_export_show_user_to_iostar_json_string_standard_case(
    standard_show_user: ShowUser,
):
    iostar_json_string = export_show_user_to_iostar_json_string(standard_show_user)
    assert isinstance(iostar_json_string, str)


def test_export_show_user_to_iostar_json_string_incorrect_input():
    show_user = create_show_user(5)
    with pytest.raises(ValueError, match="The show is not valid"):
        export_show_user_to_iostar_json_string(show_user)


def test_export_show_user_to_iostar_json_gcs_string_standard_case(
    standard_show_user: ShowUser,
):
    iostar_json_gcs_string = export_show_user_to_iostar_json_gcs_string(
        standard_show_user
    )
    assert isinstance(iostar_json_gcs_string, str)


def test_export_show_user_to_iostar_json_gcs_string_incorrect_input():
    show_user = create_show_user(5)
    with pytest.raises(ValueError, match="The show is not valid"):
        export_show_user_to_iostar_json_gcs_string(show_user)


def test_global_check_iostar_json_standard_case(
    standard_show_user: ShowUser,
):
    iostar_json_gcs = sp_to_ijg_procedure(su_to_sp_procedure(standard_show_user))
    assert global_check_iostar_json_gcs(iostar_json_gcs)
