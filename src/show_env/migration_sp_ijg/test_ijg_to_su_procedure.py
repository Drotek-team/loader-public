from ..show_user.show_user_generator import ShowUserConfiguration, get_valid_show_user
from .ijg_to_su_procedure import ijg_to_su_procedure
from .su_to_ijg_procedure import su_to_ijg_procedure


def test_ijg_to_su_procedure():
    # IMPROVE: Not ideal to test the import with the export but it is kind of impossible to visualize unitary binary data
    show_user = get_valid_show_user(ShowUserConfiguration(nb_x=2, step=2.0))
    export_import_show_px4 = ijg_to_su_procedure(su_to_ijg_procedure(show_user))
    assert show_user == export_import_show_px4
