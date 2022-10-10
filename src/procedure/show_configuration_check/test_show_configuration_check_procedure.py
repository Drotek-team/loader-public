# import os

# import pytest

# from ...drones_px4.drone_px4.drone_px4 import DronePx4
# from ...drones_px4.drones_px4 import DronesPx4
# from ...parameter.parameter import Parameter
# from ...show_user.show_user import ShowConfiguration
# from .IJ_param_check_procedure import (
#     apply_family_check_procedure,
# )
# from .IJ_param_check_report import (
#     ShowConfigurationCheckReport,
# )
# import numpy as np


# @pytest.fixture
# def invalid_drones_px4_inverse_first_positions():
#     drone_1 = DronePx4(0)
#     drone_1.add_position(0, (-100, 100, 0))
#     drone_2 = DronePx4(1)
#     drone_2.add_position(0, (100, -100, 0))
#     drone_3 = DronePx4(2)
#     drone_3.add_position(0, (100, 100, 0))
#     drone_4 = DronePx4(3)
#     drone_4.add_position(0, (-100, -100, 0))
#     return DronesPx4([drone_1, drone_2, drone_3, drone_4])


# @pytest.fixture
# def valid_show_configuration_angle():
#     return ShowConfiguration(
#         nb_x=2,
#         nb_y=2,
#         nb_drone_per_family=1,
#         step_takeoff=200,
#         angle_takeoff=45,
#         show_duration_second=0,
#         altitude_range_meter=[0, 10],
#     )


# @pytest.fixture
# def invalid_show_configuration_drone_per_family():
#     return ShowConfiguration(
#         nb_x=2,
#         nb_y=2,
#         nb_drone_per_family=2,
#         step_takeoff=200,
#         angle_takeoff=0,
#         show_duration_second=0,
#         altitude_range_meter=[0, 10],
#     )


# def test_valid_drone_manager_family():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     show_configuration_check_report = ShowConfigurationCheckReport()
#     # Define drones_px4
#     drone_1 = DronePx4(0)
#     drone_1.add_position(0, (-100, -100, 0))
#     drone_2 = DronePx4(1)
#     drone_2.add_position(0, (-100, 100, 0))
#     drone_3 = DronePx4(2)
#     drone_3.add_position(0, (100, -100, 0))
#     drone_4 = DronePx4(3)
#     drone_4.add_position(0, (100, 100, 0))
#     valid_drones_px4 = DronesPx4([drone_1, drone_2, drone_3, drone_4])
#     # Define show_configuration
#     valid_show_configuration = ShowConfiguration(
#         **{
#             "nb_x": 2,
#             "nb_y": 2,
#             "nb_drone_per_family": 1,
#             "step_takeoff": 2.0,
#             "angle_takeoff": 0,
#         }
#     )
#     apply_family_check_procedure(
#         valid_drones_px4,
#         valid_show_configuration,
#         parameter.frame_parameter,
#         parameter.iostar_json_configuration_parameter,
#         show_configuration_check_report,
#     )
#     assert show_configuration_check_report.validation


# def test_valid_drones_px4_family_angle():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())
#     angle_radian = 45
#     new_distance = np.sqrt(2)
#     drone_1 = DronePx4(0)
#     drone_1.add_position(0, (-int(new_distance * 100), 0, 0))
#     drone_2 = DronePx4(1)
#     drone_2.add_position(0, (0, int(new_distance * 100), 0))
#     drone_3 = DronePx4(2)
#     drone_3.add_position(0, (0, -int(new_distance * 100), 0))
#     drone_4 = DronePx4(3)
#     drone_4.add_position(
#         0,
#         (int(new_distance * 100), 0, 0),
#     )
#     valid_drones_px4_angle = DronesPx4([drone_1, drone_2, drone_3, drone_4])
#     valid_show_configuration_angle = ShowConfiguration(
#         nb_x=2,
#         nb_y=2,
#         nb_drone_per_family=1,
#         step_takeoff=2.0,
#         angle_takeoff=angle_radian,
#         show_duration_second=valid_drones_px4_angle.duration
#         * parameter.frame_parameter.json_fps,
#         altitude_range_meter=valid_drones_px4_angle.altitude_range,
#     )
#     show_configuration_check_report = ShowConfigurationCheckReport()
#     apply_family_check_procedure(
#         valid_drones_px4_angle,
#         valid_show_configuration_angle,
#         parameter.frame_parameter,
#         parameter.iostar_json_configuration_parameter,
#         show_configuration_check_report,
#     )
#     assert show_configuration_check_report.validation


# def test_invalid_drone_manager_first_positions():
#     parameter = Parameter()
#     parameter.load_parameter(os.getcwd())

#     # Define drones_px4
#     drone_1 = DronePx4(0)
#     drone_1.add_position(0, (-100, 100, 0))
#     drone_2 = DronePx4(1)
#     drone_2.add_position(0, (100, -100, 0))
#     drone_3 = DronePx4(2)
#     drone_3.add_position(0, (100, 100, 0))
#     drone_4 = DronePx4(3)
#     drone_4.add_position(0, (-100, -99, 0))
#     invalid_first_position_drones_px4 = DronesPx4([drone_1, drone_2, drone_3, drone_4])

#     # Define show_configuration
#     valid_show_configuration = ShowConfiguration(
#         nb_x=2,
#         nb_y=2,
#         nb_drone_per_family=1,
#         step_takeoff=2.0,
#         angle_takeoff=0,
#         show_duration_second=invalid_first_position_drones_px4.duration
#         * parameter.frame_parameter.json_fps,
#         altitude_range_meter=invalid_first_position_drones_px4.altitude_range,
#     )
#     show_configuration_check_report = ShowConfigurationCheckReport()
#     apply_family_check_procedure(
#         invalid_first_position_drones_px4,
#         valid_show_configuration,
#         parameter.frame_parameter,
#         parameter.iostar_json_configuration_parameter,
#         show_configuration_check_report,
#     )
#     assert not (
#         show_configuration_check_report.show_configuration_logic_check_report.validation
#     )