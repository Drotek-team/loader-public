import pytest
from ..show_user.show_user import ShowUser
from .export_procedure import apply_export_procedure
from ..parameter.parameter import Parameter
import os
from .export_report import ExportReport

NB_X = 20
NB_Y = 20
NB_DRONE_PER_FAMILY = 1
STEP_TAKEOFF = 1.0
ANGLE_TAKEOFF = 0


# def test_valid_show_user_json(valid_show_user_json: ShowUser):
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     export_report = ExportReport()
#     # raise ValueError(show_user_json)
#     apply_export_procedure(show_user_json["show"], export_report, parameter)
#     assert True
