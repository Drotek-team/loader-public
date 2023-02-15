from loader.check.base import get_report_validation
from loader.check.collision_check.show_position_frames_collision_check import (
    get_collision_report,
)
from loader.parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)

EPSILON_DELTA = 1e-2


def test_valid_simulation_on_ground() -> None:
    valid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground,
        ),
    )

    collision_report = get_collision_report(
        valid_show_user_on_ground,
    )

    assert get_report_validation(collision_report)


def test_invalid_simulation_on_ground() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground - EPSILON_DELTA,
        ),
    )
    collision_report = get_collision_report(
        invalid_show_user_on_ground,
    )
    assert get_report_validation(collision_report)


def test_valid_simulation_in_air() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER.security_distance_in_air,
        ),
    )
    collision_report = get_collision_report(
        invalid_show_user_on_ground,
    )
    assert get_report_validation(collision_report)


def test_invalid_simulation_in_air() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=1,
            nb_drone_per_family=2,
            step=IOSTAR_PHYSIC_PARAMETER.security_distance_in_air - EPSILON_DELTA,
        ),
    )
    collision_report = get_collision_report(
        invalid_show_user_on_ground,
    )
    assert not (get_report_validation(collision_report))
    if collision_report is None:
        msg = "Collision report is None"
        raise ValueError(msg)
    collision_infractions = collision_report.collision_infractions
    assert len(collision_infractions) == 6120
    for collision_infraction in collision_infractions:
        assert collision_infraction.in_air
