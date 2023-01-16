from ..show_px4.show_px4 import *
from .ijg_to_sp_procedure import ijg_to_sp_procedure
from .sp_to_ijg_procedure import sp_to_ijg_procedure


def test_ijg_to_sp_procedure():
    first_drone_px4 = DronePx4(0)
    first_drone_px4.add_position(0, (-100, -100, 0))
    first_drone_px4.add_position(20_000, (-100, -100, 0))
    second_drone_px4 = DronePx4(1)
    second_drone_px4.add_position(0, (100, 100, 0))
    second_drone_px4.add_position(10_000, (100, 100, 0))
    show_px4 = ShowPx4([first_drone_px4, second_drone_px4])
    # Not ideal to test the import with the export but it is kind of impossible to visualize unitary binary data
    export_import_show_px4 = ijg_to_sp_procedure(sp_to_ijg_procedure(show_px4))
    assert show_px4 == export_import_show_px4
