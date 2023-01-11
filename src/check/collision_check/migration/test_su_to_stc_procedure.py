import pytest

from migration.simulation.position_simulation import SimulationInfo
from parameter.iostar_flight_parameter.iostar_takeoff_parameter import TAKEOFF_PARAMETER
from show_user.show_user import *

from .su_to_stc_procedure import *


def test_get_position_info_from_simulation_infos():
    simulation_infos = [
        SimulationInfo(0, np.array([0.0, 0.0, 0.0]), in_air=False, in_dance=False),
        SimulationInfo(1, np.array([0.0, 0.0, 0.0]), in_air=False, in_dance=False),
        SimulationInfo(2, np.array([0.0, 0.0, 0.0]), in_air=False, in_dance=False),
    ]
    position_infos = get_position_info_from_simulation_infos(simulation_infos)
    assert position_infos == [
        CollisionPositionInfo(0, np.array([0.0, 0.0, 0.0]), in_air=False),
        CollisionPositionInfo(1, np.array([0.0, 0.0, 0.0]), in_air=False),
        CollisionPositionInfo(2, np.array([0.0, 0.0, 0.0]), in_air=False),
    ]


@pytest.fixture
def valid_show_user():
    drone_user = DroneUser(
        position_events=[
            PositionEventUser(frame=0, xyz=(0.0, 0.0, 0.0)),
            PositionEventUser(
                frame=FRAME_PARAMETER.from_absolute_time_to_absolute_frame(
                    TAKEOFF_PARAMETER.takeoff_duration_second
                ),
                xyz=(0.0, 0.0, TAKEOFF_PARAMETER.takeoff_altitude_meter_min),
            ),
        ],
        color_events=[],
        fire_events=[],
    )
    return ShowUser(drones_user=[drone_user])


def test_su_to_stc_procedure(valid_show_user: ShowUser):
    show_trajectory = su_to_stc_procedure(valid_show_user)
    assert show_trajectory.drone_number == 1
    assert len(show_trajectory.frames) == 301
    assert show_trajectory.frames == list(range(301))
    assert show_trajectory.frames == list(range(301))
