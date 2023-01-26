from ...parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ...parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from ...show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)
from .show_trajectory_performance_check import (
    apply_show_trajectory_performance_check_procedure,
)

EPSILON_DELTA = 1e-2


def test_valid_show_trajectory_performance():
    show_trajectory_performance_contenor = (
        apply_show_trajectory_performance_check_procedure(
            get_valid_show_user(ShowUserConfiguration()),
        )
    )
    assert show_trajectory_performance_contenor.user_validation


def test_valid_show_user_vertical_position():
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            takeoff_altitude=TAKEOFF_PARAMETER.takeoff_altitude_meter_min
        )
    )
    show_trajectory_performance_contenor = (
        apply_show_trajectory_performance_check_procedure(
            valid_show_user,
        )
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 960"]
    assert len(performance_infractions._error_messages) == 0  # type: ignore[test env]


def test_invalid_show_user_vertical_position():
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            takeoff_altitude=TAKEOFF_PARAMETER.takeoff_altitude_meter_min
            - EPSILON_DELTA
        )
    )
    show_trajectory_performance_contenor = (
        apply_show_trajectory_performance_check_procedure(
            valid_show_user,
        )
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 960"]
    assert len(performance_infractions._error_messages) == 1  # type: ignore[test env]
    assert (
        performance_infractions["vertical position"].display_message()
        == "[Performance Infraction] The performance vertical position has the value: 0.99 (min: 1.0) at the frame 960"
    )


def test_valid_show_user_horizontal_velocity():
    valid_show_user = get_valid_show_user(ShowUserConfiguration())
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0]
            + IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max,
            last_position_event.xyz[1],
            last_position_event.xyz[2],
        ),
    )
    show_trajectory_performance_contenor = (
        apply_show_trajectory_performance_check_procedure(
            valid_show_user,
        )
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) == 1  # type: ignore[test env]
    assert (
        performance_infractions["acceleration"].display_message()
        == "[Performance Infraction] The performance acceleration has the value: 6.00 (max: 2.0) at the frame 984"
    )


def test_invalid_show_user_horizontal_velocity():
    valid_show_user = get_valid_show_user(ShowUserConfiguration())
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0]
            + IOSTAR_PHYSIC_PARAMETER.horizontal_velocity_max
            + EPSILON_DELTA,
            last_position_event.xyz[1],
            last_position_event.xyz[2],
        ),
    )
    show_trajectory_performance_contenor = (
        apply_show_trajectory_performance_check_procedure(
            valid_show_user,
        )
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) >= 1  # type: ignore[test env]
    assert (
        performance_infractions["horizontal velocity"].display_message()
        == "[Performance Infraction] The performance horizontal velocity has the value: 6.01 (max: 6.0) at the frame 984"
    )


def test_valid_show_user_up_velocity():
    valid_show_user = get_valid_show_user(ShowUserConfiguration())
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0],
            last_position_event.xyz[1],
            last_position_event.xyz[2] + IOSTAR_PHYSIC_PARAMETER.velocity_up_max,
        ),
    )
    show_trajectory_performance_contenor = (
        apply_show_trajectory_performance_check_procedure(
            valid_show_user,
        )
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) == 1  # type: ignore[test env]
    assert (
        performance_infractions["acceleration"].display_message()
        == "[Performance Infraction] The performance acceleration has the value: 4.00 (max: 2.0) at the frame 984"
    )


def test_invalid_show_user_up_velocity():
    valid_show_user = get_valid_show_user(ShowUserConfiguration())
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0],
            last_position_event.xyz[1],
            last_position_event.xyz[2]
            + IOSTAR_PHYSIC_PARAMETER.velocity_up_max
            + EPSILON_DELTA,
        ),
    )
    show_trajectory_performance_contenor = (
        apply_show_trajectory_performance_check_procedure(
            valid_show_user,
        )
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) >= 1  # type: ignore[test env]
    assert (
        performance_infractions["up velocity"].display_message()
        == "[Performance Infraction] The performance up velocity has the value: 4.01 (max: 4.0) at the frame 984"
    )


def test_valid_show_user_down_velocity():
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            takeoff_altitude=IOSTAR_PHYSIC_PARAMETER.velocity_down_max + 1
        )
    )
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0],
            last_position_event.xyz[1],
            last_position_event.xyz[2] - IOSTAR_PHYSIC_PARAMETER.velocity_down_max,
        ),
    )
    show_trajectory_performance_contenor = (
        apply_show_trajectory_performance_check_procedure(
            valid_show_user,
        )
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) == 1  # type: ignore[test env]
    assert (
        performance_infractions["acceleration"].display_message()
        == "[Performance Infraction] The performance acceleration has the value: 4.00 (max: 2.0) at the frame 984"
    )


def test_invalid_show_user_down_velocity():
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            takeoff_altitude=IOSTAR_PHYSIC_PARAMETER.velocity_down_max + 1
        )
    )
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0],
            last_position_event.xyz[1],
            last_position_event.xyz[2]
            - IOSTAR_PHYSIC_PARAMETER.velocity_down_max
            - EPSILON_DELTA,
        ),
    )
    show_trajectory_performance_contenor = (
        apply_show_trajectory_performance_check_procedure(
            valid_show_user,
        )
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) >= 1  # type: ignore[test env]
    assert (
        performance_infractions["down velocity"].display_message()
        == "[Performance Infraction] The performance down velocity has the value: 4.01 (max: 4.0) at the frame 984"
    )


def test_valid_show_user_acceleration():
    valid_show_user = get_valid_show_user(ShowUserConfiguration())
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0],
            last_position_event.xyz[1],
            last_position_event.xyz[2],
        ),
    )
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 48,
        xyz=(
            last_position_event.xyz[0] + IOSTAR_PHYSIC_PARAMETER.acceleration_max,
            last_position_event.xyz[1],
            last_position_event.xyz[2],
        ),
    )
    show_trajectory_performance_contenor = (
        apply_show_trajectory_performance_check_procedure(
            valid_show_user,
        )
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 1008"]
    assert len(performance_infractions._error_messages) == 0  # type: ignore[test env]


def test_invalid_show_user_acceleration():
    valid_show_user = get_valid_show_user(ShowUserConfiguration())
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0],
            last_position_event.xyz[1],
            last_position_event.xyz[2],
        ),
    )
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 48,
        xyz=(
            last_position_event.xyz[0]
            + IOSTAR_PHYSIC_PARAMETER.acceleration_max
            + EPSILON_DELTA,
            last_position_event.xyz[1],
            last_position_event.xyz[2],
        ),
    )
    show_trajectory_performance_contenor = (
        apply_show_trajectory_performance_check_procedure(
            valid_show_user,
        )
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 1008"]
    assert len(performance_infractions._error_messages) == 1  # type: ignore[test env]
    assert (
        performance_infractions["acceleration"].display_message()
        == "[Performance Infraction] The performance acceleration has the value: 2.01 (max: 2.0) at the frame 1008"
    )
