from typing import Tuple
from ...drones_px4.drones_px4 import DronesPx4
from ...drones_px4.drone_px4.drone_px4 import DronePx4
from ...show_simulation.drone_simulation import DroneSimulation, PositionEventSimulation
from ...drones_px4.drone_px4.events.position_events import PositionEvent
from ..migration_DP_DU.data_convertion_format import XyzConvertionStandard
import pytest
from .DP_to_DS_procedure import DP_to_DS_procedure

ARBITRARY_INDEX = 0

FIRST_ARBITRARY_FRAME = 0
FIRST_ARBITRARY_XYZ = (1, 2, 3)

SECOND_ARBITRARY_FRAME = 240
SECOND_ARBITRARY_XYZ = (10, 20, 30)

THIRD_ARBITRARY_FRAME = 360
THIRD_ARBITRARY_XYZ = (100, 200, 300)

XYZ_CONVERTION_STANDARD = XyzConvertionStandard()


@pytest.fixture
def valid_drones_px4():
    drone = DronePx4(ARBITRARY_INDEX)
    drone.add_position(FIRST_ARBITRARY_FRAME, FIRST_ARBITRARY_XYZ)
    drone.add_position(SECOND_ARBITRARY_FRAME, SECOND_ARBITRARY_XYZ)
    drone.add_position(THIRD_ARBITRARY_FRAME, THIRD_ARBITRARY_XYZ)
    return DronesPx4([drone])


def check_drone_simulation(drone_simulation: DroneSimulation, index: int) -> bool:
    return drone_simulation.drone_index == index


def check_drone_simulation_frame_by_index(
    drone_simulation: DroneSimulation, index: int, frame: int
) -> bool:
    return drone_simulation.get_frame_by_index(index) == frame


def check_drone_simulation_position_by_index(
    drone_simulation: DroneSimulation, index: int, px4_position: Tuple[int, int, int]
) -> bool:

    return drone_simulation.get_position_by_index(
        index
    ) == XYZ_CONVERTION_STANDARD.from_px4_xyz_to_user_xyz(px4_position)


def test_DP_to_DS_procedure_standard(valid_drones_px4: DronesPx4):
    drones_simulation = DP_to_DS_procedure(valid_drones_px4)
    drone_simulation = drones_simulation[0]

    assert check_drone_simulation(drone_simulation, ARBITRARY_INDEX)
    assert check_drone_simulation_frame_by_index(
        drone_simulation, index=0, frame=FIRST_ARBITRARY_FRAME
    )
    assert check_drone_simulation_position_by_index(
        drone_simulation, index=0, px4_position=FIRST_ARBITRARY_XYZ
    )

    assert check_drone_simulation_frame_by_index(
        drone_simulation, index=1, frame=SECOND_ARBITRARY_FRAME
    )
    assert check_drone_simulation_position_by_index(
        drone_simulation, index=1, px4_position=SECOND_ARBITRARY_XYZ
    )

    assert check_drone_simulation_frame_by_index(
        drone_simulation, index=2, frame=THIRD_ARBITRARY_FRAME
    )
    assert check_drone_simulation_position_by_index(
        drone_simulation, index=2, px4_position=THIRD_ARBITRARY_XYZ
    )
