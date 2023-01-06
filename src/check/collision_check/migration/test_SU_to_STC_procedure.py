import pytest

from ....migration.simulation.position_simulation import SimulationInfo
from ....parameter.iostar_flight_parameter.iostar_takeoff_parameter import (
    TAKEOFF_PARAMETER,
)
from ....show_user.show_user import *
from .SU_to_STC_procedure import *


def test_get_position_info_from_simulation_infos():
    simulation_infos = [
        SimulationInfo(0, np.array([0.0, 0.0, 0.0]), False, False),
        SimulationInfo(1, np.array([0.0, 0.0, 0.0]), False, False),
        SimulationInfo(2, np.array([0.0, 0.0, 0.0]), False, False),
    ]
    position_infos = get_position_info_from_simulation_infos(simulation_infos)
    assert position_infos == [
        CollisionPositionInfo(0, np.array([0.0, 0.0, 0.0]), False),
        CollisionPositionInfo(1, np.array([0.0, 0.0, 0.0]), False),
        CollisionPositionInfo(2, np.array([0.0, 0.0, 0.0]), False),
    ]


@pytest.fixture
def valid_show_user():
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(position_frame=0, absolute_time=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                position_frame=int(
                    FRAME_PARAMETER.position_fps
                    * TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                absolute_time=TAKEOFF_PARAMETER.takeoff_duration_second,
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[drone_user])


def test_SU_to_STC_procedure(valid_show_user: ShowUser):
    show_trajectory = SU_to_STC_procedure(valid_show_user)
    assert show_trajectory.drone_number == 1
    assert show_trajectory.frames == [frame for frame in range(51)]
