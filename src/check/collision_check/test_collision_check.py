from ...parameter.iostar_dance_import_parameter.frame_parameter import FRAME_PARAMETER
from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from ...show_env.show_user.show_user import *
from .show_simulation_collision_check_procedure import (
    apply_show_simulation_collision_check_procedure,
)

EPSILON_DELTA = 1e-2
ROUNDING_ERROR = 0.04


def get_show_user(distance_between_drones: float) -> ShowUser:
    first_drone_user = DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_second_to_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    second_drone_user = DroneUser(
        position_events=[
            PositionEventUser(
                frame=0,
                xyz=(distance_between_drones, 0.0, 0.0),
            ),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_second_to_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(
                    distance_between_drones,
                    0.0,
                    TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
                ),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[first_drone_user, second_drone_user])


def test_valid_simulation_on_ground():
    valid_show_user_on_ground = get_show_user(
        IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground
    )
    simulation_collision_contenor = apply_show_simulation_collision_check_procedure(
        valid_show_user_on_ground,
    )
    assert (
        len(simulation_collision_contenor._error_messages) == 300  # type:ignore[test]
    )


def test_invalid_simulation_on_ground():
    invalid_show_user_on_ground = get_show_user(
        IOSTAR_PHYSIC_PARAMETER.security_distance_on_ground - EPSILON_DELTA
    )
    simulation_collision_contenor = apply_show_simulation_collision_check_procedure(
        invalid_show_user_on_ground,
    )
    first_simulation_collision_slice = (
        simulation_collision_contenor._error_messages[  # type:ignore[test]
            "Collision slice check report at frame 0"
        ]
    )
    last_simulation_collision_slice = (
        simulation_collision_contenor._error_messages[  # type:ignore[test]
            "Collision slice check report at frame 50"
        ]
    )
    assert not (first_simulation_collision_slice.user_validation)
    assert not (last_simulation_collision_slice.user_validation)


def test_valid_simulation_in_air():
    valid_show_user_in_air = get_show_user(
        IOSTAR_PHYSIC_PARAMETER.security_distance_in_air
    )
    simulation_collision_contenor = apply_show_simulation_collision_check_procedure(
        valid_show_user_in_air,
    )
    assert simulation_collision_contenor.user_validation


def test_invalid_simulation_in_air():
    invalid_show_user_in_air = get_show_user(
        IOSTAR_PHYSIC_PARAMETER.security_distance_in_air - EPSILON_DELTA
    )
    simulation_collision_contenor = apply_show_simulation_collision_check_procedure(
        invalid_show_user_in_air,
    )
    assert (
        len(simulation_collision_contenor._error_messages) == 300  # type:ignore[test]
    )
