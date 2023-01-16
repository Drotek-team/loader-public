from ..show_px4.show_px4 import *
from .sp_to_ijg_procedure import get_family_from_drones_px4, sp_to_ijg_procedure


def test_get_family_from_drones_px4_standard_case():
    first_drone_px4 = DronePx4(0)
    first_drone_px4.add_position(0, (100, 100, 0))
    second_drone_px4 = DronePx4(1)
    second_drone_px4.add_position(0, (100, 100, 0))
    family_from_drone_px4 = get_family_from_drones_px4(
        [first_drone_px4, second_drone_px4]
    )
    assert len(family_from_drone_px4.drones) == 2
    assert family_from_drone_px4.x == 100
    assert family_from_drone_px4.y == 100
    assert family_from_drone_px4.z == 0


def test_sp_to_ijg_procedure_standard_case():
    first_drone_px4 = DronePx4(0)
    first_drone_px4.add_position(0, (-100, -100, 0))
    first_drone_px4.add_position(20_000, (-100, -100, 0))
    second_drone_px4 = DronePx4(1)
    second_drone_px4.add_position(0, (100, 100, 0))
    second_drone_px4.add_position(10_000, (100, 100, 0))
    show_px4 = ShowPx4([first_drone_px4, second_drone_px4])
    iostar_json_gcs = sp_to_ijg_procedure(show_px4)
    assert len(iostar_json_gcs.show.families) == 2