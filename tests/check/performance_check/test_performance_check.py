from typing import cast

from loader.check.performance_check.show_trajectory_performance_check import (
    apply_show_trajectory_performance_check,
)
from loader.parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from loader.parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from loader.report.report import Contenor
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)

EPSILON_DELTA = 1e-2


def test_valid_show_trajectory_performance() -> None:
    show_trajectory_performance_contenor = apply_show_trajectory_performance_check(
        get_valid_show_user(ShowUserConfiguration()),
    )
    assert show_trajectory_performance_contenor.user_validation


def test_valid_show_user_vertical_position() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            takeoff_altitude=TAKEOFF_PARAMETER.takeoff_altitude_meter_min,
        ),
    )
    show_trajectory_performance_contenor = apply_show_trajectory_performance_check(
        valid_show_user,
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 960"]
    assert len(performance_infractions._error_messages) == 0  # pyright: ignore


def test_invalid_show_user_vertical_position() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            takeoff_altitude=TAKEOFF_PARAMETER.takeoff_altitude_meter_min
            - EPSILON_DELTA,
        ),
    )
    show_trajectory_performance_contenor = apply_show_trajectory_performance_check(
        valid_show_user,
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 960"]
    assert len(performance_infractions._error_messages) == 1  # pyright: ignore
    assert (
        performance_infractions["vertical position"].display_message()
        == "[Performance Infraction] The drone 0 has the performance vertical position has the value: 0.99 (min: 1.0) at the frame 960 \n"
    )


def test_valid_show_user_horizontal_velocity() -> None:
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
    show_trajectory_performance_contenor = apply_show_trajectory_performance_check(
        valid_show_user,
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) == 1  # pyright: ignore
    assert (
        performance_infractions["acceleration"].display_message()
        == "[Performance Infraction] The drone 0 has the performance acceleration has the value: 6.00 (max: 2.0) at the frame 984 \n"
    )


def test_invalid_show_user_horizontal_velocity() -> None:
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
    show_trajectory_performance_contenor = apply_show_trajectory_performance_check(
        valid_show_user,
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) >= 1  # pyright: ignore
    assert (
        performance_infractions["horizontal velocity"].display_message()
        == "[Performance Infraction] The drone 0 has the performance horizontal velocity has the value: 6.01 (max: 6.0) at the frame 984 \n"
    )


def test_valid_show_user_up_velocity() -> None:
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
    show_trajectory_performance_contenor = apply_show_trajectory_performance_check(
        valid_show_user,
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) == 1  # pyright: ignore
    assert (
        performance_infractions["acceleration"].display_message()
        == "[Performance Infraction] The drone 0 has the performance acceleration has the value: 4.00 (max: 2.0) at the frame 984 \n"
    )


def test_invalid_show_user_up_velocity() -> None:
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
    show_trajectory_performance_contenor = apply_show_trajectory_performance_check(
        valid_show_user,
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) >= 1  # pyright: ignore
    assert (
        performance_infractions["up velocity"].display_message()
        == "[Performance Infraction] The drone 0 has the performance up velocity has the value: 4.01 (max: 4.0) at the frame 984 \n"
    )


def test_valid_show_user_down_velocity() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            takeoff_altitude=IOSTAR_PHYSIC_PARAMETER.velocity_down_max + 1,
        ),
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
    show_trajectory_performance_contenor = apply_show_trajectory_performance_check(
        valid_show_user,
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) == 1  # pyright: ignore
    assert (
        performance_infractions["acceleration"].display_message()
        == "[Performance Infraction] The drone 0 has the performance acceleration has the value: 4.00 (max: 2.0) at the frame 984 \n"
    )


def test_invalid_show_user_down_velocity() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            takeoff_altitude=IOSTAR_PHYSIC_PARAMETER.velocity_down_max + 1,
        ),
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
    show_trajectory_performance_contenor = apply_show_trajectory_performance_check(
        valid_show_user,
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 984"]
    assert len(performance_infractions._error_messages) >= 1  # pyright: ignore
    assert (
        performance_infractions["down velocity"].display_message()
        == "[Performance Infraction] The drone 0 has the performance down velocity has the value: 4.01 (max: 4.0) at the frame 984 \n"
    )


def test_valid_show_user_acceleration() -> None:
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
    show_trajectory_performance_contenor = apply_show_trajectory_performance_check(
        valid_show_user,
    )
    performance_infractions = show_trajectory_performance_contenor[
        "drone trajectory performance 0"
    ]["Performance evaluation at frame 1008"]
    assert len(performance_infractions._error_messages) == 0  # pyright: ignore


def test_invalid_show_user_acceleration() -> None:
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
    show_trajectory_performance_contenor = apply_show_trajectory_performance_check(
        valid_show_user,
    )
    performance_infractions = cast(
        Contenor,
        show_trajectory_performance_contenor["drone trajectory performance 0"][
            "Performance evaluation at frame 1008"
        ],
    )
    assert (
        len(
            performance_infractions._error_messages,  # pyright: ignore[reportPrivateUsage]
        )
        == 1
    )
    assert (
        performance_infractions["acceleration"].display_message()
        == "[Performance Infraction] The drone 0 has the performance acceleration has the value: 2.01 (max: 2.0) at the frame 1008 \n"
    )
