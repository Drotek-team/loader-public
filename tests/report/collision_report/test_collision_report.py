from loader.parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER_MAX
from loader.report.base import get_report_validation
from loader.report.collision_report.show_position_frames_collision_report import (
    CollisionReport,
)
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
            step=IOSTAR_PHYSIC_PARAMETER_MAX.security_distance_on_ground,
            show_duration_absolute_time=3,
        ),
    )

    collision_report = CollisionReport.generate(
        valid_show_user_on_ground,
    )

    assert get_report_validation(collision_report)


def test_invalid_simulation_on_ground() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER_MAX.security_distance_on_ground - EPSILON_DELTA,
        ),
    )
    collision_report = CollisionReport.generate(
        invalid_show_user_on_ground,
    )
    assert get_report_validation(collision_report)


def test_valid_simulation_in_air() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER_MAX.security_distance_in_air,
        ),
    )
    collision_report = CollisionReport.generate(
        invalid_show_user_on_ground,
    )
    assert get_report_validation(collision_report)


def test_invalid_simulation_in_air() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=1,
            nb_drone_per_family=2,
            step=IOSTAR_PHYSIC_PARAMETER_MAX.security_distance_in_air - EPSILON_DELTA,
            show_duration_absolute_time=3,
        ),
    )
    collision_report = CollisionReport.generate(
        invalid_show_user_on_ground,
    )
    assert not get_report_validation(collision_report)
    assert collision_report is not None
    collision_infractions = collision_report.collision_infractions
    assert len(collision_infractions) == 2232
    for collision_infraction in collision_infractions:
        assert collision_infraction.in_air
