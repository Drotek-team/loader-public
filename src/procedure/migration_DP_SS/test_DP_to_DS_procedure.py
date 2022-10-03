from typing import List
from ...drones_px4.drones_px4 import DronesPx4
from ...drones_px4.drone_px4.drone_px4 import DronePx4
from ...show_simulation.drone_simulation import DroneSimulation, PositionEventSimulation
from ...drones_px4.drone_px4.events.position_events import PositionEvent
from ..migration_DP_DU.data_convertion_format import XyzConvertionStandard
import pytest
from .DP_to_DS_procedure import DP_to_DS_procedure


FIRST_ARBITRARY_FRAME = 0
FIRST_ARBITRARY_XYZ = (1, 2, 3)

SECOND_ARBITRARY_FRAME = 240
SECOND_ARBITRARY_XYZ = (10, 20, 30)

THIRD_ARBITRARY_FRAME = 360
THIRD_ARBITRARY_XYZ = (100, 200, 300)


@pytest.fixture
def valid_drones_px4():
    drone = DronePx4(0)
    drone.add_position(FIRST_ARBITRARY_FRAME, FIRST_ARBITRARY_XYZ)
    drone.add_position(SECOND_ARBITRARY_FRAME, SECOND_ARBITRARY_XYZ)
    drone.add_position(THIRD_ARBITRARY_FRAME, THIRD_ARBITRARY_XYZ)
    return DronesPx4([drone])


def test_DP_to_DS_procedure_standard(valid_drones_px4: DronesPx4):
    drones_simulation = DP_to_DS_procedure(valid_drones_px4)
    xyz_convertion_standard = XyzConvertionStandard()
    drone_simulation = drones_simulation[0]

    assert drone_simulation.drone_index == 0

    assert drone_simulation.get_frame_by_index(0) == FIRST_ARBITRARY_FRAME
    assert drone_simulation.get_position_by_index(
        0
    ) == xyz_convertion_standard.from_px4_xyz_to_user_xyz(FIRST_ARBITRARY_XYZ)

    assert drone_simulation.get_frame_by_index(1) == SECOND_ARBITRARY_FRAME
    assert drone_simulation.get_position_by_index(
        1
    ) == xyz_convertion_standard.from_px4_xyz_to_user_xyz(SECOND_ARBITRARY_XYZ)

    assert drone_simulation.get_frame_by_index(2) == THIRD_ARBITRARY_FRAME
    assert drone_simulation.get_position_by_index(
        2
    ) == xyz_convertion_standard.from_px4_xyz_to_user_xyz(THIRD_ARBITRARY_XYZ)
