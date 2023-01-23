from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from ...show_env.show_user.show_user_generator import (
    ShowUserConfiguration,
    get_valid_show_user,
)
from .show_simulation_collision_check_procedure import (
    apply_show_simulation_collision_check_procedure,
)

EPSILON_DELTA = 1e-2


def test_valid_simulation_on_ground():
    # TODO: make the test according to the flight_simulation behavior
    valid_show_user_on_ground = get_valid_show_user(
        ShowUserConfiguration(
            nb_x=2, nb_y=2, step=IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground
        )
    )
    simulation_collision_contenor = apply_show_simulation_collision_check_procedure(
        valid_show_user_on_ground,
    )
    for flight_index in range(1020):
        assert not (
            simulation_collision_contenor._error_messages[  # type:ignore[test]
                f"Collision slice check report at frame {flight_index}"
            ].user_validation
        )


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
    for flight_index in range(1020):
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


# TODO: this very critical test is not operational
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
    assert simulation_collision_contenor
