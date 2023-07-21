import pytest
from loader.parameters import IOSTAR_PHYSIC_PARAMETERS_MAX, IostarPhysicParameters
from loader.reports import PerformanceInfraction, PerformanceReport
from loader.reports.performance_report.performance_infraction import PerformanceKind
from loader.schemas.show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user

EPSILON_DELTA = 1e-2


def test_valid_show_trajectory_performance() -> None:
    performance_report = PerformanceReport.generate(
        get_valid_show_user(ShowUserConfiguration()),
    )
    assert not len(performance_report)


def test_valid_show_user_horizontal_velocity() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration())
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0] + IOSTAR_PHYSIC_PARAMETERS_MAX.horizontal_velocity_max,
            last_position_event.xyz[1],
            last_position_event.xyz[2],
        ),
    )
    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
    ).performance_infractions
    assert len(performance_infractions) == 1
    assert performance_infractions[0] == PerformanceInfraction(
        performance_name="acceleration",
        drone_index=0,
        frame=984,
        value=5.0,
    )


def test_invalid_show_user_horizontal_velocity() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration())
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0]
            + IOSTAR_PHYSIC_PARAMETERS_MAX.horizontal_velocity_max
            + EPSILON_DELTA,
            last_position_event.xyz[1],
            last_position_event.xyz[2],
        ),
    )
    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
    ).performance_infractions
    assert len(performance_infractions) == 1
    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
        is_partial=True,
    ).performance_infractions
    assert len(performance_infractions) == 2
    assert performance_infractions[0] == PerformanceInfraction(
        performance_name="horizontal velocity",
        drone_index=0,
        frame=984,
        value=5.01,
    )


def test_valid_show_user_up_velocity() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration())
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0],
            last_position_event.xyz[1],
            last_position_event.xyz[2] + IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_up_max,
        ),
    )
    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
    ).performance_infractions
    assert len(performance_infractions) == 1
    assert performance_infractions[0] == PerformanceInfraction(
        performance_name="acceleration",
        drone_index=0,
        frame=984,
        value=4.0,
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
            + IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_up_max
            + EPSILON_DELTA,
        ),
    )
    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
    ).performance_infractions
    assert len(performance_infractions) == 1
    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
        is_partial=True,
    ).performance_infractions
    assert len(performance_infractions) == 2
    assert performance_infractions[0] == PerformanceInfraction(
        performance_name="up velocity",
        drone_index=0,
        frame=984,
        value=4.01,
    )


def test_valid_show_user_down_velocity() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            takeoff_altitude=IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_down_max + 1,
        ),
    )
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0],
            last_position_event.xyz[1],
            last_position_event.xyz[2] - IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_down_max,
        ),
    )
    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
    ).performance_infractions
    assert len(performance_infractions) == 1
    assert performance_infractions[0] == PerformanceInfraction(
        performance_name="acceleration",
        drone_index=0,
        frame=984,
        value=4.0,
    )


def test_invalid_show_user_down_velocity() -> None:
    valid_show_user = get_valid_show_user(
        ShowUserConfiguration(
            takeoff_altitude=IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_down_max,
        ),
    )
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0],
            last_position_event.xyz[1],
            last_position_event.xyz[2]
            - IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_down_max
            - EPSILON_DELTA,
        ),
    )
    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
    ).performance_infractions
    assert len(performance_infractions) == 1
    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
        is_partial=True,
    ).performance_infractions
    assert len(performance_infractions) == 2
    assert performance_infractions[0] == PerformanceInfraction(
        performance_name="down velocity",
        drone_index=0,
        frame=984,
        value=4.01,
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
            last_position_event.xyz[0] + IOSTAR_PHYSIC_PARAMETERS_MAX.acceleration_max,
            last_position_event.xyz[1],
            last_position_event.xyz[2],
        ),
    )
    performance_report = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
    )
    assert not len(performance_report)


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
            + IOSTAR_PHYSIC_PARAMETERS_MAX.acceleration_max
            + EPSILON_DELTA,
            last_position_event.xyz[1],
            last_position_event.xyz[2],
        ),
    )
    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
    ).performance_infractions
    assert len(performance_infractions) == 0
    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IOSTAR_PHYSIC_PARAMETERS_MAX,
        is_partial=True,
    ).performance_infractions
    assert len(performance_infractions) == 1
    assert performance_infractions[0] == PerformanceInfraction(
        performance_name="acceleration",
        drone_index=0,
        frame=1008,
        value=2.01,
    )


def test_invalid_physic_parameters() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration())

    with pytest.raises(ValueError, match=" is greater than "):
        PerformanceReport.generate(
            valid_show_user,
            physic_parameters=IostarPhysicParameters(
                horizontal_velocity_max=IOSTAR_PHYSIC_PARAMETERS_MAX.horizontal_velocity_max + 0.5,
            ),
        )

    with pytest.raises(ValueError, match=" is greater than "):
        PerformanceReport.generate(
            valid_show_user,
            physic_parameters=IostarPhysicParameters(
                velocity_up_max=IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_up_max + 0.5,
            ),
        )

    with pytest.raises(ValueError, match=" is greater than "):
        PerformanceReport.generate(
            valid_show_user,
            physic_parameters=IostarPhysicParameters(
                velocity_down_max=IOSTAR_PHYSIC_PARAMETERS_MAX.velocity_down_max + 0.5,
            ),
        )

    with pytest.raises(ValueError, match=" is greater than "):
        PerformanceReport.generate(
            valid_show_user,
            physic_parameters=IostarPhysicParameters(
                acceleration_max=IOSTAR_PHYSIC_PARAMETERS_MAX.acceleration_max + 0.5,
            ),
        )


def test_valid_physic_parameters() -> None:
    valid_show_user = get_valid_show_user(ShowUserConfiguration())
    last_position_event = valid_show_user.drones_user[0].position_events[-1]
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 24,
        xyz=(
            last_position_event.xyz[0] + 0.5,
            last_position_event.xyz[1],
            last_position_event.xyz[2] + 0.5,
        ),
    )
    valid_show_user.drones_user[0].add_position_event(
        frame=last_position_event.frame + 48,
        xyz=(
            last_position_event.xyz[0],
            last_position_event.xyz[1],
            last_position_event.xyz[2],
        ),
    )

    assert not len(PerformanceReport.generate(valid_show_user))

    performance_infractions = PerformanceReport.generate(
        valid_show_user,
        physic_parameters=IostarPhysicParameters(
            velocity_up_max=0.4,
            velocity_down_max=0.4,
            acceleration_max=0.5,
            horizontal_velocity_max=0.4,
        ),
    ).performance_infractions
    assert all(
        kind.value in [infractions.performance_name for infractions in performance_infractions]
        for kind in PerformanceKind
    )
