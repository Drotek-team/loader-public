import numpy as np
from loader.report.simulation.in_dance_flight_simulation import (
    in_dance_flight_simulation,
)
from loader.report.simulation.position_simulation import SimulationInfo
from loader.show_env.show_user import PositionEventUser


def test_in_air_flight_simulation_explanation() -> None:
    valid_position_events_user = [
        PositionEventUser(frame=0, xyz=(0.0, 2.0, 0.0)),
        PositionEventUser(frame=1, xyz=(2.0, 4.0, 1.0)),
        PositionEventUser(frame=3, xyz=(4.0, 8.0, 2.0)),
    ]

    real_in_air_flight_simulation_infos = in_dance_flight_simulation(
        valid_position_events_user,
    )
    assert real_in_air_flight_simulation_infos[0] == SimulationInfo(
        frame=0,
        position=np.array((0.0, 2.0, 0.0)),
        in_air=True,
    )
    assert real_in_air_flight_simulation_infos[1] == SimulationInfo(
        frame=1,
        position=np.array((2.0, 4.0, 1.0)),
        in_air=True,
    )
    assert real_in_air_flight_simulation_infos[2] == SimulationInfo(
        frame=2,
        position=np.array((3.0, 6.0, 1.5)),
        in_air=True,
    )


def test_in_air_flight_simulation_rounding_principle() -> None:
    valid_position_events_user = [
        PositionEventUser(frame=0, xyz=(1.88888888, 2.2222222, 0.4444444)),
        PositionEventUser(frame=2, xyz=(2.88888888, 4.2222222, 1.4444444)),
    ]
    real_in_air_flight_simulation_infos = in_dance_flight_simulation(
        valid_position_events_user,
    )
    assert real_in_air_flight_simulation_infos[0] == SimulationInfo(
        frame=0,
        position=np.array((1.889, 2.222, 0.444)),
        in_air=True,
    )
    assert real_in_air_flight_simulation_infos[1] == SimulationInfo(
        frame=1,
        position=np.array((2.389, 3.222, 0.944)),
        in_air=True,
    )
