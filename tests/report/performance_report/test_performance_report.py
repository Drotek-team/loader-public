from loader.parameter.iostar_physic_parameter import IOSTAR_PHYSIC_PARAMETER
from loader.report.base import get_report_validation
from loader.report.performance_report.show_trajectory_performance_report import (
    PerformanceInfraction,
    PerformanceReport,
)
from loader.show_env.show_user.generate_show_user import (
    ShowUserConfiguration,
    get_valid_show_user,
)

EPSILON_DELTA = 1e-2


def test_valid_show_trajectory_performance() -> None:
    performance_report = PerformanceReport.generate(
        get_valid_show_user(ShowUserConfiguration()),
    )
    assert get_report_validation(performance_report)


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
    performance_report = PerformanceReport.generate(
        valid_show_user,
    )
    if performance_report is None:
        msg = "Performance report is None"
        raise ValueError(msg)

    performance_infractions = performance_report.performance_infractions
    assert len(performance_infractions) == 1
    assert (
        performance_infractions[0].dict()
        == PerformanceInfraction(
            performance_name="acceleration",
            drone_index=0,
            frame=984,
            value=5.0,
            threshold=2.0,
        ).dict()
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
    performance_report = PerformanceReport.generate(
        valid_show_user,
    )
    if performance_report is None:
        msg = "Performance report is None"
        raise ValueError(msg)

    performance_infractions = performance_report.performance_infractions
    assert len(performance_infractions) == 2
    assert (
        performance_infractions[0].dict()
        == PerformanceInfraction(
            performance_name="horizontal velocity",
            drone_index=0,
            frame=984,
            value=5.01,
            threshold=5.0,
        ).dict()
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
    performance_report = PerformanceReport.generate(
        valid_show_user,
    )
    if performance_report is None:
        msg = "Performance report is None"
        raise ValueError(msg)

    performance_infractions = performance_report.performance_infractions
    assert len(performance_infractions) == 1
    assert (
        performance_infractions[0].dict()
        == PerformanceInfraction(
            performance_name="acceleration",
            drone_index=0,
            frame=984,
            value=4.0,
            threshold=2.0,
        ).dict()
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
    performance_report = PerformanceReport.generate(
        valid_show_user,
    )
    if performance_report is None:
        msg = "Performance report is None"
        raise ValueError(msg)
    performance_infractions = performance_report.performance_infractions
    assert len(performance_infractions) == 2
    assert (
        performance_infractions[0].dict()
        == PerformanceInfraction(
            performance_name="up velocity",
            drone_index=0,
            frame=984,
            value=4.01,
            threshold=4.0,
        ).dict()
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
    performance_report = PerformanceReport.generate(
        valid_show_user,
    )
    if performance_report is None:
        msg = "Performance report is None"
        raise ValueError(msg)

    performance_infractions = performance_report.performance_infractions
    assert len(performance_infractions) == 1
    assert (
        performance_infractions[0].dict()
        == PerformanceInfraction(
            performance_name="acceleration",
            drone_index=0,
            frame=984,
            value=4.0,
            threshold=2.0,
        ).dict()
    )


def test_invalid_show_user_down_velocity() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            takeoff_altitude=IOSTAR_PHYSIC_PARAMETER.velocity_down_max,
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
    performance_report = PerformanceReport.generate(
        valid_show_user,
    )
    if performance_report is None:
        msg = "Performance report is None"
        raise ValueError(msg)
    performance_infractions = performance_report.performance_infractions
    assert len(performance_infractions) == 2
    assert (
        performance_infractions[0].dict()
        == PerformanceInfraction(
            performance_name="down velocity",
            drone_index=0,
            frame=984,
            value=4.01,
            threshold=4.0,
        ).dict()
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
    performance_report = PerformanceReport.generate(
        valid_show_user,
    )
    assert get_report_validation(performance_report)


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
    performance_report = PerformanceReport.generate(
        valid_show_user,
    )
    if performance_report is None:
        msg = "Performance report is None"
        raise ValueError(msg)
    performance_infractions = performance_report.performance_infractions
    assert len(performance_infractions) == 1
    assert (
        performance_infractions[0].dict()
        == PerformanceInfraction(
            performance_name="acceleration",
            drone_index=0,
            frame=1008,
            value=2.01,
            threshold=2.0,
        ).dict()
    )
