from loader.parameter.iostar_physic_parameter import (
    IOSTAR_PHYSIC_PARAMETER_MAX,
    IOSTAR_PHYSIC_PARAMETER_RECOMMENDATION,
)
from loader.report.base import get_report_validation
from loader.report.collision_report.show_position_frames_collision_report import (
    CollisionReport,
)
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)

EPSILON_DELTA = 1e-2


def test_collision_report_valid() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
        ),
    )
    collision_report = CollisionReport.generate(invalid_show_user_on_ground)
    assert get_report_validation(collision_report)


def test_collision_report_invalid() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER_RECOMMENDATION.security_distance_in_air - EPSILON_DELTA,
            show_duration_absolute_time=3,
        ),
    )
    collision_report = CollisionReport.generate(invalid_show_user_on_ground)
    assert not get_report_validation(collision_report)
    assert collision_report is not None
    collision_infractions = collision_report.collision_infractions
    assert len(collision_infractions) == 1488
    for collision_infraction in collision_infractions:
        assert collision_infraction.in_air

    collision_report = CollisionReport.generate(
        invalid_show_user_on_ground,
        physic_parameter=IOSTAR_PHYSIC_PARAMETER_MAX,
    )
    assert get_report_validation(collision_report)
