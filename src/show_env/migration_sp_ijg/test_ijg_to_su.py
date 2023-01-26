from ..show_user.generate_show_user import ShowUserConfiguration, get_valid_show_user
from .ijg_to_su import ijg_to_su
from .su_to_ijg import su_to_ijg


def test_ijg_to_su():
    # IMPROVE: Not ideal to test the import with the export but it is kind of impossible to visualize unitary binary data
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, step=2.0))
    export_import_show_px4 = ijg_to_su(su_to_ijg(show_user))
    assert show_user == export_import_show_px4
