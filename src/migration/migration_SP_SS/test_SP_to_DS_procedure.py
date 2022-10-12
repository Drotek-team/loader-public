from typing import Tuple
from ...show_px4.show_px4 import ShowPx4
from ...show_px4.drone_px4.drone_px4 import DronePx4
from ...show_dev.show_dev import DroneDev

from ..migration_SP_SU.data_convertion_format import XyzConvertionStandard
import pytest
from .SP_to_DS_procedure import SP_to_SD_procedure

ARBITRARY_INDEX = 0

FIRST_ARBITRARY_FRAME = 0
FIRST_ARBITRARY_XYZ = (1, 2, 3)

SECOND_ARBITRARY_FRAME = 240
SECOND_ARBITRARY_XYZ = (10, 20, 30)

THIRD_ARBITRARY_FRAME = 360
THIRD_ARBITRARY_XYZ = (100, 200, 300)

XYZ_CONVERTION_STANDARD = XyzConvertionStandard()


@pytest.fixture
def valid_show_px4():
    drone = DronePx4(ARBITRARY_INDEX)
    drone.add_position(FIRST_ARBITRARY_FRAME, FIRST_ARBITRARY_XYZ)
    drone.add_position(SECOND_ARBITRARY_FRAME, SECOND_ARBITRARY_XYZ)
    drone.add_position(THIRD_ARBITRARY_FRAME, THIRD_ARBITRARY_XYZ)
    return ShowPx4([drone])


def check_drone_dev(drone_dev: DroneDev, index: int) -> bool:
    return drone_dev.drone_index == index


def check_drone_dev_frame_by_index(drone_dev: DroneDev, index: int, frame: int) -> bool:
    return drone_dev.get_frame_by_index(index) == frame


def check_drone_dev_position_by_index(
    drone_dev: DroneDev, index: int, px4_position: Tuple[int, int, int]
) -> bool:

    return drone_dev.get_xyz_simulation_by_index(
        index
    ) == XYZ_CONVERTION_STANDARD.from_px4_xyz_to_user_xyz(px4_position)


def test_SP_to_SD_procedure_standard(valid_show_px4: ShowPx4):
    drones_dev = SP_to_SD_procedure(valid_show_px4)
    drone_dev = drones_dev[0]

    assert check_drone_dev(drone_dev, ARBITRARY_INDEX)
    assert check_drone_dev_frame_by_index(
        drone_dev, index=0, frame=FIRST_ARBITRARY_FRAME
    )
    assert check_drone_dev_position_by_index(
        drone_dev, index=0, px4_position=FIRST_ARBITRARY_XYZ
    )

    assert check_drone_dev_frame_by_index(
        drone_dev, index=1, frame=SECOND_ARBITRARY_FRAME
    )
    assert check_drone_dev_position_by_index(
        drone_dev, index=1, px4_position=SECOND_ARBITRARY_XYZ
    )

    assert check_drone_dev_frame_by_index(
        drone_dev, index=2, frame=THIRD_ARBITRARY_FRAME
    )
    assert check_drone_dev_position_by_index(
        drone_dev, index=2, px4_position=THIRD_ARBITRARY_XYZ
    )
