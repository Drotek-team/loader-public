from ...show_env.show_user.show_user import DroneUser
from .flight_simulation import get_flight_simulation
from .in_air_flight_simulation import in_air_flight_simulation
from .land_simulation import land_simulation
from .stand_by_simulation import stand_by_simulation
from .takeoff_simulation import takeoff_simulation


def test_flight_simulation_standard_case():
    drone_user = DroneUser(position_events=[], color_events=[], fire_events=[])
    drone_user.add_position_event(0, (0.0, 0.0, 0.0))
    drone_user.add_position_event(240, (0.0, 0.0, 1.0))
    drone_user.add_position_event(360, (2.0, 0.0, 1.0))

    flight_simulation = get_flight_simulation(drone_user)
    assert len(flight_simulation) == 421
    assert flight_simulation[:239] == takeoff_simulation(
        drone_user.position_events[0].xyz, drone_user.position_events[0].frame
    )
    assert flight_simulation[239:360] == in_air_flight_simulation(
        drone_user.flight_positions
    )
    assert flight_simulation[360:420] == land_simulation(
        drone_user.position_events[-1].xyz, 360
    )
    assert flight_simulation[420] == stand_by_simulation(420, 421, (2.0, 0.0, 0.0))[0]


def test_flight_simulation_takeoff_delayed():
    takeoff_delay = 100
    drone_user = DroneUser(position_events=[], color_events=[], fire_events=[])
    drone_user.add_position_event(0 + takeoff_delay, (0.0, 0.0, 0.0))
    drone_user.add_position_event(240 + takeoff_delay, (0.0, 0.0, 1.0))
    drone_user.add_position_event(360 + takeoff_delay, (2.0, 0.0, 1.0))
    flight_simulation = get_flight_simulation(drone_user)

    assert len(flight_simulation) == 521
    assert flight_simulation[:takeoff_delay] == stand_by_simulation(
        0, drone_user.position_events[0].frame, drone_user.position_events[0].xyz
    )
    assert flight_simulation[takeoff_delay : 239 + takeoff_delay] == takeoff_simulation(
        drone_user.position_events[0].xyz, drone_user.position_events[0].frame
    )
    assert flight_simulation[
        takeoff_delay + 239 : takeoff_delay + 360
    ] == in_air_flight_simulation(drone_user.flight_positions)
    assert flight_simulation[
        takeoff_delay + 360 : takeoff_delay + 420
    ] == land_simulation(
        drone_user.position_events[-1].xyz, drone_user.position_events[-1].frame
    )
    assert flight_simulation[520] == stand_by_simulation(520, 521, (2.0, 0.0, 0.0))[0]


def test_flight_simulation_last_frame_delayed():
    last_frame_delayed = 1000
    drone_user = DroneUser(position_events=[], color_events=[], fire_events=[])
    drone_user.add_position_event(0, (0.0, 0.0, 0.0))
    drone_user.add_position_event(240, (0.0, 0.0, 1.0))
    drone_user.add_position_event(360, (2.0, 0.0, 1.0))

    flight_simulation = get_flight_simulation(drone_user, last_frame_delayed)
    assert len(flight_simulation) == last_frame_delayed
    assert flight_simulation[:239] == takeoff_simulation(
        drone_user.position_events[0].xyz, drone_user.position_events[0].frame
    )
    assert flight_simulation[239:360] == in_air_flight_simulation(
        drone_user.flight_positions
    )
    assert flight_simulation[360:420] == land_simulation(
        drone_user.position_events[-1].xyz, 360
    )
    last_simulation = land_simulation(drone_user.position_events[-1].xyz, 360)[-1]
    assert flight_simulation[420 : last_frame_delayed + 1] == stand_by_simulation(
        last_simulation.frame + 1,
        last_frame_delayed,
        (2.0, 0.0, 0.0),
    )


def test_flight_simulation_non_takeoff():
    drone_user = DroneUser(position_events=[], color_events=[], fire_events=[])
    drone_user.add_position_event(240, (0.0, 0.0, 0.0))
    flight_simulation = get_flight_simulation(drone_user)

    assert len(flight_simulation) == 241
    assert flight_simulation[:241] == stand_by_simulation(
        0, drone_user.position_events[0].frame + 1, drone_user.position_events[0].xyz
    )


def test_flight_simulation_non_takeoff_last_frame_delayed():
    last_frame_delayed = 1000
    drone_user = DroneUser(position_events=[], color_events=[], fire_events=[])
    drone_user.add_position_event(240, (0.0, 0.0, 0.0))
    flight_simulation = get_flight_simulation(drone_user, last_frame_delayed)

    assert len(flight_simulation) == last_frame_delayed
    assert flight_simulation[:last_frame_delayed] == stand_by_simulation(
        0, last_frame_delayed, drone_user.position_events[0].xyz
    )
