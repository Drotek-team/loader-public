import pytest

from src.show_env.show_px4.show_px4 import DronePx4, ShowPx4

from ..migration_sp_su.sp_to_su_procedure import sp_to_su_procedure
from .su_to_sc_procedure import su_to_sc_procedure


@pytest.fixture
def valid_one_drone_show_px4():
    drone_px4 = DronePx4(0)
    drone_px4.add_position(0, (0, 0, 0))
    drone_px4.add_position(1000, (0, 0, -10))
    return ShowPx4([drone_px4])


# TODO hypothesis for that
def test_sp_to_sc_procedure_one_drone(valid_one_drone_show_px4: ShowPx4):
    show_configuration = su_to_sc_procedure(
        sp_to_su_procedure(valid_one_drone_show_px4)
    )
    assert show_configuration.nb_x == 1
    assert show_configuration.nb_y == 1
    assert show_configuration.nb_drone_per_family == 1
    assert show_configuration.step == 0
    assert show_configuration.angle_takeoff == 0
    assert show_configuration.duration == 1
    assert show_configuration.hull == [(0, 0)]
    assert show_configuration.altitude_range == (0, 0)
