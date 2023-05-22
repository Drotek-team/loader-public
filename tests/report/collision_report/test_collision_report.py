from loader.parameters import (
    IOSTAR_PHYSIC_PARAMETERS_MAX,
    IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION,
)
from loader.reports import CollisionReport
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user

EPSILON_DELTA = 1e-2


def test_collision_report_valid() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
        ),
    )
    collision_report = CollisionReport.generate(invalid_show_user_on_ground)
    assert not len(collision_report)


def test_collision_report_invalid() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETERS_RECOMMENDATION.security_distance_in_air - EPSILON_DELTA,
            show_duration_absolute_time=3,
        ),
    )
    collision_report = CollisionReport.generate(invalid_show_user_on_ground)
    assert len(collision_report)
    assert collision_report is not None
    collision_infractions = collision_report.collision_infractions
    assert len(collision_infractions) == 1488
    for collision_infraction in collision_infractions:
        assert collision_infraction.in_air

    collision_report = CollisionReport.generate(
        invalid_show_user_on_ground,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
    )
    assert not len(collision_report)
