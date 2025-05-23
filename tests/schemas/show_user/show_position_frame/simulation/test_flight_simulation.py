import numpy as np
import pytest
from loader.schemas.show_user import DroneUser
from loader.schemas.show_user.show_position_frame.simulation.flight_simulation import (
    SimulationInfo,
    get_flight_simulation,
    get_partial_flight_simulation,
)
from loader.schemas.show_user.show_position_frame.simulation.in_dance_flight_simulation import (
    in_dance_flight_simulation,
)
from loader.schemas.show_user.show_position_frame.simulation.land_simulation import land_simulation
from loader.schemas.show_user.show_position_frame.simulation.stand_by_simulation import (
    stand_by_simulation,
)
from loader.schemas.show_user.show_position_frame.simulation.takeoff_simulation import (
    takeoff_simulation,
)


def test_flight_simulation_standard_case() -> None:
    drone_user = DroneUser(
        index=0,
        position_events=[],
        color_events=[],
        fire_events=[],
        yaw_events=[],
    )
    drone_user.add_position_event(0, (0.0, 0.0, 0.0))
    drone_user.add_position_event(240, (0.0, 0.0, 1.0))
    drone_user.add_position_event(360, (2.0, 0.0, 1.0))

    flight_simulation = get_flight_simulation(drone_user)
    assert len(flight_simulation) == 421
    assert flight_simulation[:240] == takeoff_simulation(
        drone_user.position_events[0].xyz,
        drone_user.position_events[1].xyz,
        drone_user.position_events[0].frame,
        drone_user.position_events[1].frame,
    )
    assert flight_simulation[240:360] == in_dance_flight_simulation(
        drone_user.flight_positions,
    )
    assert flight_simulation[360:420] == land_simulation(
        drone_user.position_events[-1].xyz,
        360,
    )
    assert flight_simulation[420] == SimulationInfo(
        frame=420,
        position=np.array([2.0, 0.0, 0.0], dtype=np.float64),
    )


def test_flight_simulation_takeoff_delayed() -> None:
    takeoff_delay = 100
    drone_user = DroneUser(
        index=0,
        position_events=[],
        color_events=[],
        fire_events=[],
        yaw_events=[],
    )
    drone_user.add_position_event(takeoff_delay + 0, (0.0, 0.0, 0.0))
    drone_user.add_position_event(takeoff_delay + 240, (0.0, 0.0, 1.0))
    drone_user.add_position_event(takeoff_delay + 360, (2.0, 0.0, 1.0))
    flight_simulation = get_flight_simulation(drone_user)

    assert len(flight_simulation) == 521
    assert flight_simulation[:takeoff_delay] == stand_by_simulation(
        0,
        drone_user.position_events[0].frame,
        drone_user.position_events[0].xyz,
    )
    assert flight_simulation[takeoff_delay : takeoff_delay + 240] == takeoff_simulation(
        drone_user.position_events[0].xyz,
        drone_user.position_events[1].xyz,
        drone_user.position_events[0].frame,
        drone_user.position_events[1].frame,
    )
    assert flight_simulation[
        takeoff_delay + 240 : takeoff_delay + 360
    ] == in_dance_flight_simulation(drone_user.flight_positions)
    assert flight_simulation[takeoff_delay + 360 : takeoff_delay + 420] == land_simulation(
        drone_user.position_events[-1].xyz,
        takeoff_delay + 360,
    )
    assert flight_simulation[takeoff_delay + 420] == SimulationInfo(
        frame=520,
        position=np.array([2.0, 0.0, 0.0], dtype=np.float64),
    )


def test_flight_simulation_last_frame_delayed() -> None:
    last_frame_delayed = 1000
    drone_user = DroneUser(
        index=0,
        position_events=[],
        color_events=[],
        fire_events=[],
        yaw_events=[],
    )
    drone_user.add_position_event(0, (0.0, 0.0, 0.0))
    drone_user.add_position_event(240, (0.0, 0.0, 1.0))
    drone_user.add_position_event(360, (2.0, 0.0, 1.0))

    flight_simulation = get_flight_simulation(drone_user, last_frame_delayed)
    assert len(flight_simulation) == last_frame_delayed + 1
    assert flight_simulation[:240] == takeoff_simulation(
        drone_user.position_events[0].xyz,
        drone_user.position_events[1].xyz,
        drone_user.position_events[0].frame,
        drone_user.position_events[1].frame,
    )
    assert flight_simulation[240:360] == in_dance_flight_simulation(
        drone_user.flight_positions,
    )
    assert flight_simulation[360:420] == land_simulation(
        drone_user.position_events[-1].xyz,
        360,
    )
    last_simulation_info = land_simulation(drone_user.position_events[-1].xyz, 360)[-1]
    assert flight_simulation[420 : last_frame_delayed + 1] == stand_by_simulation(
        last_simulation_info.frame + 1,
        last_frame_delayed + 1,
        (2.0, 0.0, 0.0),
    )


def test_flight_simulation_non_takeoff() -> None:
    drone_user = DroneUser(
        index=0,
        position_events=[],
        color_events=[],
        fire_events=[],
        yaw_events=[],
    )
    with pytest.raises(
        ValueError,
        match="Drone user must have at least 2 position events",
    ):
        get_flight_simulation(drone_user)

    drone_user.add_position_event(240, (0.0, 0.0, 0.0))
    with pytest.raises(
        ValueError,
        match="Drone user must have at least 2 position events",
    ):
        get_flight_simulation(drone_user)


def test_partial_flight_simulation_standard_case() -> None:
    drone_user = DroneUser(
        index=0,
        position_events=[],
        color_events=[],
        fire_events=[],
        yaw_events=[],
    )
    drone_user.add_position_event(0, (0.0, 0.0, 1.0))
    drone_user.add_position_event(120, (2.0, 0.0, 1.0))

    partial_flight_simulation = get_partial_flight_simulation(drone_user)
    assert len(partial_flight_simulation) == 120
    assert partial_flight_simulation[0] == SimulationInfo(
        frame=0,
        position=np.array([0.0, 0.0, 1.0], dtype=np.float64),
    )
    assert partial_flight_simulation[60] == SimulationInfo(
        frame=60,
        position=np.array([1.0, 0.0, 1.0], dtype=np.float64),
    )
    assert partial_flight_simulation[119] == SimulationInfo(
        frame=119,
        position=np.array([1.983, 0.0, 1.0], dtype=np.float64),
    )
