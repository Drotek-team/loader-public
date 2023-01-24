from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from ...show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)
from .show_simulation_collision_check_procedure import (
    apply_show_simulation_collision_check_procedure,
)

EPSILON_DELTA = 1e-2


def test_valid_simulation_on_ground():
    valid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2, nb_y=2, step=IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground
        )
    )
    simulation_collision_contenor = apply_show_simulation_collision_check_procedure(
        valid_show_user_on_ground,
    )
    assert (
        len(simulation_collision_contenor._error_messages) == 1020  # type:ignore[test]
    )
    for flight_index in range(1020):
        assert not (
            simulation_collision_contenor._error_messages[  # type:ignore[test]
                f"Collision slice check report at frame {flight_index}"
            ].user_validation
        )
        for (
            collision_infraction
        ) in simulation_collision_contenor._error_messages[  # type:ignore[test]
            f"Collision slice check report at frame {flight_index}"
        ]._error_messages.values():  # type:ignore[test]
            assert collision_infraction.in_air  # type:ignore[test]


def test_invalid_simulation_on_ground():
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground - EPSILON_DELTA,
        )
    )
    simulation_collision_contenor = apply_show_simulation_collision_check_procedure(
        invalid_show_user_on_ground,
    )
    assert (
        len(simulation_collision_contenor._error_messages) == 1022  # type:ignore[test]
    )
    for flight_index in range(1022):
        assert not (
            simulation_collision_contenor._error_messages[  # type:ignore[test]
                f"Collision slice check report at frame {flight_index}"
            ].user_validation
        )


def test_valid_simulation_in_air():
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER.security_distance_in_air,
        )
    )
    simulation_collision_contenor = apply_show_simulation_collision_check_procedure(
        invalid_show_user_on_ground,
    )
    assert len(simulation_collision_contenor._error_messages) == 0  # type:ignore[test]


def test_invalid_simulation_in_air():
    invalid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2,
            nb_y=2,
            step=IOSTAR_PHYSIC_PARAMETER.security_distance_in_air - EPSILON_DELTA,
        )
    )
    simulation_collision_contenor = apply_show_simulation_collision_check_procedure(
        invalid_show_user_on_ground,
    )
    assert (
        len(simulation_collision_contenor._error_messages) == 1020  # type:ignore[test]
    )
    for flight_index in range(1020):
        assert not (
            simulation_collision_contenor._error_messages[  # type:ignore[test]
                f"Collision slice check report at frame {flight_index}"
            ].user_validation
        )
        for (
            collision_infraction
        ) in simulation_collision_contenor._error_messages[  # type:ignore[test]
            f"Collision slice check report at frame {flight_index}"
        ]._error_messages.values():  # type:ignore[test]
            assert collision_infraction.in_air  # type:ignore[test]
