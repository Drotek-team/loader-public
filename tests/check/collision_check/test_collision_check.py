from loader.check.collision_check.show_simulation_collision_check import (
    apply_show_simulation_collision_check,
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
    simulation_collision_contenor = apply_show_simulation_collision_check(
        valid_show_user_on_ground,
    )
    assert (
        len(
            simulation_collision_contenor._error_messages,  # pyright: ignore[reportPrivateUsage]
        )
        == 0
    )  # pyright: ignore[reportPrivateUsage]


def test_invalid_simulation_on_ground() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground - EPSILON_DELTA,
        ),
    )
    simulation_collision_contenor = apply_show_simulation_collision_check(
        invalid_show_user_on_ground,
    )
    assert (
        len(
            simulation_collision_contenor._error_messages,  # pyright: ignore[reportPrivateUsage]
        )
        == 0
    )  # pyright: ignore[reportPrivateUsage]


def test_valid_simulation_in_air() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER.security_distance_in_air,
        ),
    )
    simulation_collision_contenor = apply_show_simulation_collision_check(
        invalid_show_user_on_ground,
    )
    assert (
        len(
            simulation_collision_contenor._error_messages,  # pyright: ignore[reportPrivateUsage]
        )
        == 0
    )


# TODO: no family in these tests
def test_invalid_simulation_in_air() -> None:
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER.security_distance_in_air - EPSILON_DELTA,
        ),
    )
    simulation_collision_contenor = apply_show_simulation_collision_check(
        invalid_show_user_on_ground,
    )
    assert (
        len(
            simulation_collision_contenor._error_messages,  # pyright: ignore[reportPrivateUsage]
        )
        == 1020
    )  # pyright: ignore[reportPrivateUsage]
    for flight_index in range(1020):
        assert not (
            simulation_collision_contenor._error_messages[  # pyright: ignore[reportPrivateUsage]
                f"Collision slice check report at frame {flight_index}"
            ].user_validation
        )
        for (
            collision_infraction
        ) in simulation_collision_contenor._error_messages[  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportPrivateUsage]
            f"Collision slice check report at frame {flight_index}"
        ]._error_messages.values():  # pyright: ignore[reportGeneralTypeIssues]
            assert (
                collision_infraction.in_air
            )  # pyright: ignore[reportUnknownMemberType]
